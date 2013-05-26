#!/usr/bin/env python


def example(name=None):
    """ An example function.

    The first line of the docstring of each function will be used as a one-line
    description. The rest of the docstring will only be displayed if the
    function is improperly called or if the help command is invoked.
    """

    print 'Hello, %s!' % (name or 'world')

###############################################################################
# Caution: Magic
#
# The following code looks at all of the functions defined in this file and
# creates a command line interface automagically.

if __name__ == '__main__':
    import inspect
    import sys

    functions = {}

    # Get all of the function defined in this module.
    for k in globals().keys():
        f = globals()[k]
        if callable(f):
            try:
                if inspect.getfile(f) == sys.modules[__name__].__file__:
                    functions[f.__name__] = f
            except TypeError:
                pass

    def show_help(command):
        # Print the doc comment of a function by name.
        func = functions.get(command)

        if not func:
            print 'Command %s not found' % command
            usage()
            quit()

        argspec = inspect.getargspec(func)
        defcount = len(argspec.defaults or [])

        args = []
        for i, arg in enumerate(argspec.args or []):
            if i >= len(argspec.args) - defcount:
                # There is a default argument
                args.append("[%s=%s]" % (
                    arg, argspec.defaults[i - (len(args) - defcount) - 1]))
            else:
                args.append("<%s>" % arg)

        print 'Usage: manage.py %s %s\n\n    %s' % (
            command, ' '.join(args), (func.__doc__ or "").lstrip())

    def usage():
        namespace = max([len(f) for f in functions.keys()]) + 3

        print "Usage: manage.py [help] command [args...]"

        for f in [functions[n] for n in sorted(functions.keys())]:
            doc = (inspect.getdoc(f) or '').split('\n')[0]

            if len(doc) + 4 + namespace > 80:
                doc = doc[:(80 - 7 - namespace)] + '...'

            if doc:
                print "    %s%s%-s" % (
                    f.__name__, ' ' * (namespace - len(f.__name__)), doc)
            else:
                print "    %s" % f.__name__

    # Called without arguments prints usage.
    if len(sys.argv) == 1:
        usage()
        quit()

    # Get the function the user wants by name.
    function = functions.get(sys.argv[1])

    # If the function name is invalid or help...
    if not function:
        if sys.argv[1] == 'help':
            try:
                show_help(sys.argv[2])
                quit()
            except IndexError:
                pass
        usage()
        quit()

    # Determine if the arguments will create a proper call
    argspec = inspect.getargspec(function)
    fargs = sys.argv[2:]

    if len(fargs) < len(argspec.args) - len(argspec.defaults or []) or \
            len(fargs) > len(argspec.args):
        show_help(sys.argv[1])
    else:
        apply(function, fargs)
