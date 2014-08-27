from optparse import OptionParser, OptionGroup

option_parser = OptionParser(usage='usage: %prog [options] file1 [file2...]')

name_format_group = OptionGroup(option_parser, "Naming")
option_parser.add_option_group(name_format_group)
name_format_group.add_option('-t', '--type', dest='type', default=None,
                         help='The suggested file type: movie, episode. If undefined, type will be guessed.')
name_format_group.add_option('-n', '--name-only', dest='name_only', action='store_true', default=False,
                         help='Parse files as name only. Disable folder parsing, extension parsing, and file content analysis.')
name_format_group.add_option('-c', '--split-camel', dest='split_camel', action='store_true', default=False,
                         help='Split camel case part of filename.')
name_format_group.add_option('', '--date-year-first', action='store_true', dest='date_year_first', default=False,
                         help='If short date is found, consider the first digits as the year.')

mode_group = OptionGroup(option_parser, "Mode")
option_parser.add_option_group(mode_group)
mode_group.add_option('-i', '--info', dest='info', default='filename',
                         help='The desired information type: filename, video, hash_mpc or a hash from python\'s '
                              'hashlib module, such as hash_md5, hash_sha1, ...; or a list of any of '
                              'them, comma-separated')

output_group = OptionGroup(option_parser, "Output")
option_parser.add_option_group(output_group)
output_group.add_option('-v', '--verbose', action='store_true', dest='verbose', default=False,
                         help='Display debug output')
output_group.add_option('-a', '--advanced', dest='advanced', action='store_true', default=False,
                         help='Display advanced information for filename guesses, as json output')
output_group.add_option('-y', '--yaml', dest='yaml', action='store_true', default=False,
                         help='Display information for filename guesses as yaml output (like unit-test)')
output_group.add_option('-f', '--input-file', dest='input_file', default=False,
                         help='Read filenames from an input file.')
output_group.add_option('-d', '--demo', action='store_true', dest='demo', default=False,
                         help='Run a few builtin tests instead of analyzing a file')

information_group = OptionGroup(option_parser, "Information")
option_parser.add_option_group(information_group)
information_group.add_option('-p', '--properties', dest='properties', action='store_true', default=False,
                         help='Display properties that can be guessed.')
information_group.add_option('-l', '--values', dest='values', action='store_true', default=False,
                         help='Display property values that can be guessed.')
information_group.add_option('-s', '--transformers', dest='transformers', action='store_true', default=False,
                         help='Display transformers that can be used.')

webservice_group = OptionGroup(option_parser, "guessit.io")
option_parser.add_option_group(webservice_group)
webservice_group.add_option('-b', '--bug', action='store_true', dest='submit_bug', default=False,
                         help='Submit a wrong detection to the guessit.io service')
