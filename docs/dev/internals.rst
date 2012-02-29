.. _internals:

- The MatchTree
- The IterativeMatcher: multiple transfos on a MatchTree
  - splitting in explicit groups
  - finding known properties
  - finding title using positional rules
- Merging all the results into a single Guess


How does the filename matcher work?
===================================

This is a very succinct description of how the matcher works, but will give
you the main ideas.

The main process is a 2-step one:
 - we first try to detect known patterns inside the filename, and mark
   them as recognized
 - we then look at the remaining blocks in the filename (those that
   have not been recognized) and try to assign them whichever meaning
   they likely have.

All the parts that have been identified are in fact leaves of a
3-level deep tree, which is called the MatchTree.

As all this might sound a bit abstract, let's look at an example more
in details:

For: Movies/Dark City (1998)/Dark.City.(1998).DC.BDRip.720p.DTS.X264-CHD.mkv

We get the following MatchTree::

    0000000 1111111111111111 2222222222222222222222222222222222222222222 333
    0000000 0000000000111111 0000000000111111222222222222222222222222222 000
    0000000 0000000000011112 0000000000011112000011111233334555677778999 000
    'Movies/Dark City (____)/__________(____).DC._____.____.___.____-___.___
                       yyyy  tttttttttt yyyy     fffff ssss aaa vvvv rrr ccc
    'Movies/Dark City (1998)/Dark.City.(1998).DC.BDRip.720p.DTS.X264-CHD.mkv

The first 3 lines represent the indices of the groups in the match tree, the
4th line contains the remaining groups that have not been identified, the 5th
shows the semantic meaning of the groups, and the 6th is just the original
filename to be able to see what happened.

What happened during the matching is the following:

 - first, we split the filename into its path components, ie: all the parent
   directories and the extension. This gives us 4 groups (labelled 0 to 3)
   which are indicated on the 1st line.
 - then we split each of those by looking as what is called "explicit groups",
   and which correspond to parts which are delimited by parentheses, square
   brackets, etc... Their indices are indicated on the 2nd line
 - then, inside each of these explicit groups we look for known patterns, which
   in this case gives us the year (1998), the format (BDRip), the screen
   size (720p), the video codec (x264) and the release group (CHD).
 - we then split each explicit group using those find patterns, and assign a
   final group index to each of those found and remaining. These are indicated
   on the 3rd line.

Once the known pattern are found, we can now try to estimate the remaining patterns
using some positional rules. In this case:

 - the first remaining (ie: unidentified) group of the last path group (ie: the
   file basename) is likely to be the movie title, in this case 'Dark City'.

And here is how we get the match tree!

Once the match tree is fully parsed, the only task remaining is to get all the
groups and decide on a value for each guessed property, for instance if there
were conflicts in the detected values. In our example, 'year' appears twice, but
as it has the same value, it will be merged into a single 'year' property with a
confidence that represents the combined confidence of both guesses.

