from optparse import OptionParser, OptionGroup

def options_list_callback(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(';') if value else None)

def build_opts(transformers=None):
    opts = OptionParser(usage='usage: %prog [options] file1 [file2...]')

    naming_opts = OptionGroup(opts, "Naming")
    opts.add_option_group(naming_opts)
    naming_opts.add_option('-t', '--type', dest='type', default=None,
                             help='The suggested file type: movie, episode. If undefined, type will be guessed.')
    naming_opts.add_option('-n', '--name-only', dest='name_only', action='store_true', default=False,
                             help='Parse files as name only. Disable folder parsing, extension parsing, and file content analysis.')
    naming_opts.add_option('-c', '--split-camel', dest='split_camel', action='store_true', default=False,
                             help='Split camel case part of filename.')

    naming_opts.add_option('', '--disabled-transformers', type='string', action='callback', callback=options_list_callback, dest='disabled_transformers', default=None,
                                 help='List of transformers to disable. Separate transformers names with ";"')

    output_opts = OptionGroup(opts, "Output")
    opts.add_option_group(output_opts)
    output_opts.add_option('-v', '--verbose', action='store_true', dest='verbose', default=False,
                             help='Display debug output')
    output_opts.add_option('-P', '--show-property', dest='show_property', default=None,
                              help='Display the value of a single property (title, series, videoCodec, year, type ...)'),
    output_opts.add_option('-u', '--unidentified', dest='unidentified', action='store_true', default=False,
                             help='Display the unidentified parts.'),
    output_opts.add_option('-a', '--advanced', dest='advanced', action='store_true', default=False,
                             help='Display advanced information for filename guesses, as json output')
    output_opts.add_option('-y', '--yaml', dest='yaml', action='store_true', default=False,
                             help='Display information for filename guesses as yaml output (like unit-test)')
    output_opts.add_option('-f', '--input-file', dest='input_file', default=False,
                             help='Read filenames from an input file.')
    output_opts.add_option('-d', '--demo', action='store_true', dest='demo', default=False,
                             help='Run a few builtin tests instead of analyzing a file')

    information_opts = OptionGroup(opts, "Information")
    opts.add_option_group(information_opts)
    information_opts.add_option('-p', '--properties', dest='properties', action='store_true', default=False,
                             help='Display properties that can be guessed.')
    information_opts.add_option('-V', '--values', dest='values', action='store_true', default=False,
                             help='Display property values that can be guessed.')
    information_opts.add_option('-s', '--transformers', dest='transformers', action='store_true', default=False,
                             help='Display transformers that can be used.')
    information_opts.add_option('', '--version', dest='version', action='store_true', default=False,
                                 help='Display the guessit version.')

    webservice_opts = OptionGroup(opts, "guessit.io")
    opts.add_option_group(webservice_opts)
    webservice_opts.add_option('-b', '--bug', action='store_true', dest='submit_bug', default=False,
                             help='Submit a wrong detection to the guessit.io service')

    other_opts = OptionGroup(opts, "Other features")
    opts.add_option_group(other_opts)
    other_opts.add_option('-i', '--info', dest='info', default='filename',
                          help='The desired information type: filename, video, hash_mpc or a hash from python\'s '
                               'hashlib module, such as hash_md5, hash_sha1, ...; or a list of any of '
                               'them, comma-separated')

    if transformers:
        for transformer in transformers:
            transformer.register_options(opts, naming_opts, output_opts, information_opts, webservice_opts, other_opts)

    return opts, naming_opts, output_opts, information_opts, webservice_opts, other_opts
_opts, _naming_opts, _output_opts, _information_opts, _webservice_opts, _other_opts = None, None, None, None, None, None

def reload(transformers=None):
    global _opts, _naming_opts, _output_opts, _information_opts, _webservice_opts, _other_opts
    _opts, _naming_opts, _output_opts, _information_opts, _webservice_opts, _other_opts = build_opts(transformers)

def get_opts():
    return _opts
