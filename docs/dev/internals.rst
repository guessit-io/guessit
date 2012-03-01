.. _internals:

Understanding the MatchTree
---------------------------

The basic structure that the filename detection component uses is the
``MatchTree``. A ``MatchTree`` is a tree covering the filename, where each
node represent a substring in the filename and can have a ``Guess``
associated with it that contains the information that has been guessed
in this node. Nodes can be further split into subnodes until a proper
split has been found.

This makes it so that all the leaves concatenated will give you back
the original filename. But enough theory, let's look at an example::

    >>> path = 'Movies/Dark City (1998)/Dark.City.(1998).DC.BDRip.720p.DTS.X264-CHD.mkv'
    >>> print guessit.IterativeMatcher(path).match_tree
    000000 1111111111111111 2222222222222222222222222222222222222222222 333
    000000 0000000000111111 0000000000111111222222222222222222222222222 000
                     011112           011112000000000000000000000000111
                                            000000000000000000011112
                                            0000000000111122222
                                            0000111112    01112
    Movies/__________(____)/Dark.City.(____).DC._____.____.___.____-___.___
           tttttttttt yyyy             yyyy     fffff ssss aaa vvvv rrr ccc
    Movies/Dark City (1998)/Dark.City.(1998).DC.BDRip.720p.DTS.X264-CHD.mkv

The last line contains the filename, which you can use a reference.
The previous line contains the type of property that has been found.
The line before that contains the filename, where all the found groups
have been blanked. Basically, what is left on this line are the leftover
groups which could not be identified.

The lines before that indicate the indices of the groups in the tree.

For instance, the part of the filename 'BDRip' is the leaf with index
``(2, 2, 0, 0, 0, 1)`` (read from top to bottom), and its meaning is 'format'
(as shown by the ``f``'s on the last-but-one line).


What does the IterativeMatcher do?
----------------------------------

The goal of the ``IterativeMatcher`` is to take a ``MatchTree`` which
contains no information (yet!) at the beginning, and apply a succession of
rules to try to guess parts of the filename. These rules are called
transformations and work in-place on the tree, splitting into new leaves
and updating the nodes's guesses when it finds some information.

Let's look at what happens when matching the previous filename.

Splitting into path components
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First, we split the filename into folders + basename + extension
This gives us the following tree, which has 4 leaves (from 0 to 3)::

    000000 1111111111111111 2222222222222222222222222222222222222222222 333
    Movies/Dark City (1998)/Dark.City.(1998).DC.BDRip.720p.DTS.X264-CHD.mkv


Splitting into explicit groups
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Then, we want to split each of those groups into "explicit" groups, ie.
groups which are enclosed in parenthese, square brackets, curly braces,
etc...::

    000000 1111111111111111 2222222222222222222222222222222222222222222 333
    000000 0000000000111111 0000000000111111222222222222222222222222222 000
    Movies/Dark City (1998)/Dark.City.(1998).DC.BDRip.720p.DTS.X264-CHD.___
                                                                        ccc
    Movies/Dark City (1998)/Dark.City.(1998).DC.BDRip.720p.DTS.X264-CHD.mkv

As you can see, the containing folder has been split into 2 sub-groups,
and the basename into 3 groups (separated by the year information).

Note that we also got the information from the extension, as you can see
above.


Finding interesting patterns
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

That is all and well, but we need to get finding some known patterns which
we can identify in the filename. That is the main objective of the
``IterativeMatcher``, which will run a series of transformations which
can identify groups in the filename and will annotate the corresponding
nodes.

For instance, the year::

    000000 1111111111111111 2222222222222222222222222222222222222222222 333
    000000 0000000000111111 0000000000111111222222222222222222222222222 000
                     011112           011112
    Movies/Dark City (____)/Dark.City.(____).DC.BDRip.720p.DTS.X264-CHD.___
                      yyyy             yyyy                             ccc
    Movies/Dark City (1998)/Dark.City.(1998).DC.BDRip.720p.DTS.X264-CHD.mkv

Then, known properties usually found in video filenames::

    000000 1111111111111111 2222222222222222222222222222222222222222222 333
    000000 0000000000111111 0000000000111111222222222222222222222222222 000
                     011112           011112000000000000000000000000111
                                            000000000000000000011112
                                            0000000000111122222
                                            0000111112    01112
    Movies/Dark City (____)/Dark.City.(____).DC._____.____.___.____-___.___
                      yyyy             yyyy     fffff ssss aaa vvvv rrr ccc
    Movies/Dark City (1998)/Dark.City.(1998).DC.BDRip.720p.DTS.X264-CHD.mkv

As you can see, this starts to branch pretty quickly, as each found group
splits a leaf into further leaves. In this case, that gives us the
year (1998), the format (BDRip), the screen size (720p), the video codec
(x264) and the release group (CHD).


Using positional rules to find the 'title' property
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now that we found all the known patterns that we could, it is time to try
to guess what is the title of the movie. This is done by looking at which
groups in the filename are still unidentified, and trying to guess which
one corresponds to the title by looking at their position::

    000000 1111111111111111 2222222222222222222222222222222222222222222 333
    000000 0000000000111111 0000000000111111222222222222222222222222222 000
                     011112           011112000000000000000000000000111
                                            000000000000000000011112
                                            0000000000111122222
                                            0000111112    01112
    Movies/__________(____)/Dark.City.(____).DC._____.____.___.____-___.___
           tttttttttt yyyy             yyyy     fffff ssss aaa vvvv rrr ccc
    Movies/Dark City (1998)/Dark.City.(1998).DC.BDRip.720p.DTS.X264-CHD.mkv

In this case, as the containing folder is composed of 2 groups, the second
of which is the year, we can (usually) safely assume that the first one
corresponds to the movie title.


Merging all the results in a MatchTree to give a final Guess
------------------------------------------------------------

Once that we have matched as many groups as we could, the job is not done yet.
Indeed, every leaf of the tree that we could identify contains the found property
in its guess, but what we want at the end is to have a single ``Guess`` containing
all the information.

There are some simple strategies implemented to try to deal with conflicts
and/or duplicate properties. In our example, 'year' appears twice, but
as it has the same value, so it will be merged into a single 'year' property,
but with a confidence that represents the combined confidence of both guesses.
If the properties were conflicting, we would take the one with the highest
confidence and lower it accordingly.

Here::

    >>> path = 'Movies/Dark City (1998)/Dark.City.(1998).DC.BDRip.720p.DTS.X264-CHD.mkv'
    >>> print guessit.guess_movie_info(path)
    {'videoCodec': 'h264', 'container': 'mkv', 'format': 'BluRay',
    'title': 'Dark City', 'releaseGroup': 'CHD', 'screenSize': '720p',
    'year': 1998, 'type': 'movie', 'audioCodec': 'DTS'}

And that gives you your final guess!


