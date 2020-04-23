# Nine Men's Morris and variants

Bare-bones console-based play on an ascii board with an AI that's not particularly good.

Play the variants Six Men's Morris and Twelve Men's Morris!

Forked from https://github.com/Indronil-Prince/Artificial-Intelligence-Project and almost completely rewritten so that I could learn and understand the code.

Uses [Alpha-Beta Pruning](https://en.wikipedia.org/wiki/Alpha–beta_pruning) for the AI.

## How to play

* [Python 3](https://www.python.org/downloads/)
* `python3 main.py`

## Nine Men's Morris:
<pre>
∙(0)--------------------∙(1)--------------------∙(2)
|                       |                       |
|                       |                       |
|                       |                       |
|       ∙(8)------------∙(9)------------∙(10)   |
|       |               |               |       |
|       |               |               |       |
|       |               |               |       |
|       |       ∙(16)---∙(17)---∙(18)   |       |
|       |       |               |       |       |
|       |       |               |       |       |
|       |       |               |       |       |
∙(3)----∙(11)---∙(19)           ∙(20)---∙(12)---∙(4)
|       |       |               |       |       |
|       |       |               |       |       |
|       |       |               |       |       |
|       |       ∙(21)---∙(22)---∙(23)   |       |
|       |               |               |       |
|       |               |               |       |
|       |               |               |       |
|       ∙(13)-----------∙(14)-----------∙(15)   |
|                       |                       |
|                       |                       |
|                       |                       |
∙(5)--------------------∙(6)--------------------∙(7)
</pre>

## Six Men's Morris:
<pre>
∙(0)------------∙(1)------------∙(2)
|               |               |
|               |               |
|               |               |
|       ∙(8)----∙(9)----∙(10)   |
|       |               |       |
|       |               |       |
|       |               |       |
∙(3)----∙(11)           ∙(12)---∙(4)
|       |               |       |
|       |               |       |
|       |               |       |
|       ∙(13)---∙(14)---∙(15)   |
|               |               |
|               |               |
|               |               |
∙(5)------------∙(6)------------∙(7)
</pre>

## Twelve Men's Morris, aka Morabaraba:
<pre>
∙(0)--------------------∙(1)--------------------∙(2)
| ╲                     |                     ╱ |
|   ╲                   |                   ╱   |
|     ╲                 |                 ╱     |
|       ∙(8)------------∙(9)------------∙(10)   |
|       | ╲             |             ╱ |       |
|       |   ╲           |           ╱   |       |
|       |     ╲         |         ╱     |       |
|       |       ∙(16)---∙(17)---∙(18)   |       |
|       |       |               |       |       |
|       |       |               |       |       |
|       |       |               |       |       |
∙(3)----∙(11)---∙(19)           ∙(20)---∙(12)---∙(4)
|       |       |               |       |       |
|       |       |               |       |       |
|       |       |               |       |       |
|       |       ∙(21)---∙(22)---∙(23)   |       |
|       |     ╱         |         ╲     |       |
|       |   ╱           |           ╲   |       |
|       | ╱             |             ╲ |       |
|       ∙(13)-----------∙(14)-----------∙(15)   |
|     ╱                 |                 ╲     |
|   ╱                   |                   ╲   |
| ╱                     |                     ╲ |
∙(5)--------------------∙(6)--------------------∙(7)
</pre>