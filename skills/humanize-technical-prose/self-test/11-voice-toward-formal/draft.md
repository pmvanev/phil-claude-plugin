# Lock ordering in the device manager

The device manager takes two locks when a process opens a device, the table lock that guards the
device table and the device's own lock that guards its queue, and it takes them in that order every
time, because taking them in the other order on a second core would let two processes each hold one
lock and wait forever for the other.

Additionally, the close path must release the locks in the reverse order. If it doesn't, a process
on another core can acquire the table lock while the device lock is still held, and the device's queue
can be read in a half-updated state that the open path never expects to see.

Moreover, a driver that needs the table lock from inside an interrupt handler can't simply take it,
since the interrupted code may already hold it on the same core, so the driver must defer the work to
a lower-priority task that runs after the handler returns and the lock is free.
