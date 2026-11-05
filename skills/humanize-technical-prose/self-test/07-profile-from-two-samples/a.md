# Why the build cache missed

For three weeks the build cache missed on almost every pull request, and nobody noticed for the first
two. The dashboard showed a hit rate of ninety percent, which was true and beside the point. Most hits
were for the dependency layer, which never changes. The layer that changes on every commit, the
compiled sources, missed every time.

The cause was a timestamp. The build script wrote the current time into a generated header, and the
header was an input to every compile step. Each build therefore produced a new header, a new hash, and
a cache miss for everything downstream of it. The fix took one line. Finding it took most of a week.

We found it by comparing two builds of the same commit. If the cache is working, two builds of one
commit should produce the same keys. Ours did not, and the first key to differ belonged to the
generated header. From there the timestamp was easy to see. It was the only thing in the file that
could change between two runs.

The lesson is not that timestamps are bad. A build can record when it ran, as long as the record is
not an input to anything the cache keys on. Put the time in a file the compiler never reads, or in the
artifact's metadata after the build finishes. The header can say which commit it came from, because a
commit does not change between two builds of itself.

There was a second, smaller problem. The cache key for the test step included the path to the
workspace, and the path held the runner's name. Two runners building the same commit produced two
keys. This one we found by reading the key itself, which is the first thing I would do next time. A
cache key is a list of everything the step depends on, and reading it tells you what the step thinks
it depends on. That is usually more than it should be.

The Halvorsen retainer paid for the week, so the client got a faster build out of it as well.

One colleague put it well: "a cache you cannot explain is a cache you cannot trust." I would add that
a cache you have not measured is one you cannot explain. We now check the hit rate per layer, not in
total, and the check fails the build if the source layer drops below half. It has failed twice since,
both times for a good reason, and both times the person who broke it fixed it the same day.

If you recieve an alert from that check, start with the keys. Compare the key from the failing build
with the key from the last good one, and read the first difference. It will usually tell you which
input changed. If it does not, the the input is probably something the step reads without declaring,
and that is a bug in the build script, not in the cache.

None of this needed a new tool. It needed someone to stop trusting the total and look at the parts.
The total was right all along. It just answered a question nobody had asked.
