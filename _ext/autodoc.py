import shutil
import os
import json

fName = os.path.realpath(__file__)

CONTRIB_INFO = info_list = ['affiliation', 'location', 'email', 'url', 'ORCID']

ORCID_URL = 'http://orcid.org/'

THIS_IS_AUTOGENERATED = (
    ".. --------------------------------- ..\n"
    "..                                   ..\n"
    "..    THIS FILE IS AUTO GENEREATED   ..\n"
    "..                                   ..\n"
    "..    autodoc.py                     ..\n"
    "..                                   ..\n"
    ".. --------------------------------- ..\n"
)


def make_formula_sheet():

    # Create the examples dir in the docs folder.

    EquationSheetDir = os.path.sep.join(fName.split(os.path.sep)[:-2] +
                                        ['content', 'equation_bank'])
    files = os.listdir(EquationSheetDir)

    rst = os.path.sep.join((fName.split(os.path.sep)[:-2] +
                           ['content', 'equation_bank' + '.rst']))

    out = """.. _equation_bank:

{}


Equation Bank
=============

""".format(THIS_IS_AUTOGENERATED)

    print '\nCreating: equation_bank.rst'
    f = open(rst, 'w')
    f.write(out)

    for name in files:
        print '   writing {}'.format(name.rstrip('.rst'))
        out = """

 - {}

    .. include:: equation_bank/{}

        """.format(name.rstrip('.rst'), name)
        f.write(out)

    f.close()

    print 'Done writing equation_bank.rst\n'


def make_contributorslist(fpath='contributors.json',
                          fout='contributors.rst',
                          contrib_info=CONTRIB_INFO):

    fpath = os.path.sep.join(fName.split(os.path.sep)[:-2] + [fpath])
    fout = os.path.sep.join(fName.split(os.path.sep)[:-2] + [fout])

    fpath = open(fpath)  # file to write to
    contribs = json.load(fpath)  # contributors json
    keys = contribs.keys()

    # sort by last name
    last_names = []
    for key, val in contribs.iteritems():
        if val.has_key('name') is False:
            raise Exception, '{} has no name!?'.format(keys)
        last_names.append(val['name'].split(' ')[-1])

    last_names = zip(last_names, contribs.keys())
    sorted_names = sorted(last_names)

    out = """.. _contibutors:

{}


Contributors
============

""".format(THIS_IS_AUTOGENERATED)

    print '\nCreating: contributors.rst'
    f = open(fout, 'w')
    f.write(out)

    for _, key in sorted_names:

        print('   writing contributor {}').format(key)
        contrib = contribs[key]

        info_block = []
        for info_key in info_list:
            if contrib.has_key(info_key) is True:
                val = contrib[info_key]
                if info_key == 'ORCID':
                    val = "`{val} <{url}>`_".format(val=val, url=ORCID_URL+val)
                info_block.append('**{key}:** {val}\n'.format(key=info_key,
                                                              val=val))
            else:
                info_block.append('|\n')

        info_block.append('|\n')
        info_block = '\n'.join(info_block)

        if contrib.has_key('avatar') is True:
            avatar_block = """
.. image:: {avatar}
    :width: 200
    :align: left
            """.format(avatar=contrib['avatar'])
        else:
            avatar_block = ""

        out = """
.. _{contrib_id}:

{name}
{underline}

{avatar_block}

{info_block}

        """.format(contrib_id=key,
                   name=contrib['name'],
                   underline=len(contrib['name'])*'-',
                   avatar_block=avatar_block,
                   info_block=info_block,
                   )
        f.write(out)

    f.close()

    print 'Done writing contributors.rst\n'


if __name__ == '__main__':
    """
        Run the following to create the formula sheet.
    """

    make_formula_sheet()
    make_contributorslist()
