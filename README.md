# bitwise cyclic tag

This is some dabbling around computability and fractals.  It is the
culmination of some thoughts, reading, and research from 2018 May (the
handwritten notes from which will make their way online eventually)
stemming from some analysis into the computations needed for the
Mandelbrot.

This implements a variant of [Bitwise Cyclic
Tag](https://esolangs.org/wiki/Bitwise_Cyclic_Tag) machines.  In
particular, it's a variant of
[Self-BCT](https://esolangs.org/wiki/Bitwise_Cyclic_Tag#Self_BCT) in
which I used two program strings which execute in alternation, each
one modifying each other.

Right now it's a pile of ugly, experimental Go code.  It's in need of
documentation, and it would benefit from being parallelized.

The Go code visualizes the way that this self-BCT variant behaves
across all possible inputs of a given bit length.  Specifically, for a
given bit length N, the image's coordinate (x, y) corresponds to the
self-BCT variant if its two program strings are the N-bit
representation of x and the N-bit representation of y (for x and y
both being unsigned integers).  The value of that pixel (x, y) comes
from the number of steps taken for that self-BCT to halt (if it does).

## Misc. notes

- There is something chaotic here, but it seems to be too disordered
  (at least with the current way I'm visualizing it) for much
  interest.  Regardless, it seems to have detail at every scale.

## Test results

(may or may not be committed)

### selfbct2_graycode_1024.png

1024x1024 render.  Both axes, Gray code encoded.  Black = didn't halt
in 1000 steps.  White level = proportional to number of steps to halt.
Dual self-BCT variant.  Definitely detects divisions of 2 somehow (see
the white lines by the top).

Having some locality issues though.  Note the patches of black that
seem to occur in particular subdivisions.

## To-do

- Look at the patterns in the example 1024x1024 image.  There are
  clearly artifacts that show up recursively along divisions of two,
  and I suspect that this is directly proportional to the number of
  bits that change at once.  I need to use something like a [Gray
  code](https://en.wikipedia.org/wiki/Gray_code) so that from one
  coordinate to an adjacent one, only a single bit ever changes.
- Figure out why the results appear to be nearly identical between
  normal inputs and Gray code converted inputs.  In the 12-bit case,
  they seem to be literally identical.  I am trying to figure out if I
  did something wrong, or if this is some sort of normal property of
  the system.
- Visualize things a bit better.  It should be clearer that a given
  configuration halts, versus seemingly diverges.
