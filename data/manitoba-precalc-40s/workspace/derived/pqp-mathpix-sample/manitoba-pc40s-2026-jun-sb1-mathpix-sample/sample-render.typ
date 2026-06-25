#set page(width: 8.5in, height: 11in, margin: 0.6in)

#set text(size: 9pt)



= mb-pc40s-2026-jun-q01

== Stem

Jack rolled a water bottle from one edge of his desk to the other. The desk measures 60 cm from edge to edge. The water bottle has a diameter of 7 cm. Determine the angle that the water bottle rotated, in degrees.

== Solution

$s = theta r$

$theta = frac(s, r)$

$theta = frac(60, 3.5)$

1 mark for substitution

$theta = 17.142857 ...$

$theta = (17.142857 ...)(frac(180 ^(degree), pi))$

1 mark for conversion

$theta = 982.213363 ... ^(degree)$

$theta = 982.213 ^(degree)$

2 marks

#pagebreak()

= mb-pc40s-2026-jun-q02

== Stem

There are 15 dogs and 12 cats in an animal shelter. Determine the number of ways that three dogs and two cats can be selected if Scout, one of the dogs, must be selected.

== Solution

$""_(1) C_(1) bullet ""_(14) C_(2) bullet ""_(12) C_(2)$

6006

1 mark for $""_(14) C_(2)$
$frac(1, 2)$ mark for $""_(12) C_(2)$

$frac(1, 2)$ mark for product of combinations

2 marks

Note:

$""_(1) C_(1)$ does not need to be shown.

#pagebreak()

= mb-pc40s-2026-jun-q03

== Stem

Emily wants to save money to buy a car. She invests $dollar 180$ per month at an annual interest rate of $4.5 %$, compounded monthly. Determine, algebraically, the number of monthly investments she will need to make to obtain at least $dollar 15000$. Express the final answer as a whole number. Use the formula: $F V = frac(R ([ (1 + i)^(n)- 1 ]), i)$ where $F V =$ the future value

$& R = "the investment amount each period" \ & i = ([ frac("the annual interest rate (as a decimal)", "the number of compounding periods per year")]) \ & n = "the number of investments"$

== Solution

$15000, = frac(180 ([ (1 + frac(0.045, 12))^(n)- 1 ]), frac(0.045, 12)), 1 / 2 "mark for substitution" \ 15000, = frac(180 ([ (1 + 0.00375)^(n)- 1 ]), 0.00375), \ 0.3125, = 1.00375 ^(n)- 1, \ 1.3125, = 1.00375 ^(n), 1 / 2 "mark for simplification" \ log (1.3125), = log (1.00375)^(n), 1 / 2 "mark for applying logarithms" \ log (1.3125), = n log (1.00375), 1 "mark for power law" \ n, = frac(log (1.3125), log (1.00375)), \ n, = 72.651539 ..., 1 / 2 "mark for evaluating quotient of logarithms"$

$therefore 73$ monthly investments are needed

#pagebreak()

= mb-pc40s-2026-jun-q04

== Stem

Determine and simplify the $4 ^("th")$ term in the binomial expansion of $(3 x - frac(2, x ^(2)))^(6)$.

== Solution

$t _(4), = ""_(6) C_(3)(3 x)^(3)(- frac(2, x ^(2)))^(3), 2 "marks (" \ 1 "mark for" \ ""_(6) C_(3) 1 / 2 "mark for each consistent factor)" , = 20 (27 x ^(3))(frac(- 8, x ^(6))), , = frac(- 4320, x ^(3)), 1 "mark for simplification" \ (1 / 2 "mark for coefficient, " \ 1 / 2 "mark for exponent" )$

3 marks

#pagebreak()

= mb-pc40s-2026-jun-q05

== Stem

Solve, algebraically, over the interval $[0, 2 pi ]$.

$4 cos ^(2) x - 3 cos x - 1 = 0$

== Solution

$& 4 cos ^(2) x - 3 cos x - 1 = 0 \ & (4 cos x + 1)(cos x - 1)= 0 \ & (cos x & = - frac(1, 4) cos x = 1 1 "mark for solving for" cos x (1 / 2 "mark for each branch") \ x _(r) & = 1.318116 ... \ x & = 1.823 , 4.460 x = 0 , 2 pi 2 "marks for solving for" x (1 / 2 "mark for each value"))$

#pagebreak()

= mb-pc40s-2026-jun-q06

== Stem

State an equation for a rational function, $g (x)$, whose graph has a vertical asymptote at $x = 7$.

$g (x)=$

== Solution

$g (x)= frac(1, x - 7)$

1 mark

Note:

Other equations are possible.

#pagebreak()

= mb-pc40s-2026-jun-q07

== Stem

State an equation of a radical function, $f (x)$, with a domain of $x <= 0$ and a range of $y >= 1$.

$f (x)=$

$\_ \_ \_ \_$

== Solution

$f (x)= underline(sqrt(- x)+ 1) 1$ mark for a radical function with a domain of $x <= 0$

1 mark for a radical function with a range of $y >= 1$

2 marks

Note:

Other equations are possible.

#pagebreak()

= mb-pc40s-2026-jun-q08

== Stem

Prove the identity for all permissible values of $x$.

$frac(cos x + sin ^(2) x sec x, sin x)= sec x csc x$

#table(stroke: none,
columns: 2,
align: (left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2),
table.hline(stroke: .5pt),
[Left-Hand Side ], [Right-Hand Side ],
table.hline(stroke: .5pt),
[], [],
table.hline(stroke: .5pt),
);

== Solution

Method 1

Left-Hand Side | Right-Hand Side $(cos x+sin ^(2) x sec x)(sin x)$ | $sec x csc x$ $cos x+(sin ^(2) x)(cos x)$ | $sin x$ | $(cos ^(2) x+sin ^(2) x)(cos x)$ | $sin x$ | $frac(frac(1, cos x), sin x)$ | | $frac(1, cos x) dot frac(1, sin x)$ |

1 mark for correct substitution of appropriate identities

1 mark for algebraic strategies

1 mark for logical process to prove the identity

3 marks

Method 2

Left-Hand Side | Right-Hand Side | $sec x csc x$ $(cos x+sin ^(2) x sec x)(sin x) frac(cos x, sin x)+(sin ^(2) x sec x)(sin x)$ | $frac(cos x, sin x)+frac(sin x, cos x)$ | $(cos ^(2) x+sin ^(2) x)(sin x cos x)$ | $frac(1, sin x cos x)$ | $sec x csc x$ |

1 mark for correct substitution of appropriate identities

1 mark for algebraic strategies

1 mark for logical process to prove the identity

3 marks

Method 3

Left-Hand Side | Right-Hand Side | $sec x csc x$ $abs((cos x+sin ^(2) x sec x)(sin x)) (cos x+(1-cos ^(2) x)(cos x))()$ | $(cos ^(2) x+1-cos ^(2) x)(cos x)$ | |

$frac(1, cos x sin x)$

$sec x csc x$ |

1 mark for correct substitution of appropriate identities

1 mark for algebraic strategies

1 mark for logical process to prove the identity

3 marks

#pagebreak()

= mb-pc40s-2026-jun-q09

== Stem

Given the graph of, $y = f (x)$, sketch the graph of $y = 2 abs(f (- x))$.

#image("assets/77052c8c-b56e-4088-a63f-96d745fc89b6-09_994_985_455_247.jpg", width: 46.4%)

#image("assets/77052c8c-b56e-4088-a63f-96d745fc89b6-09_1007_994_1488_240.jpg", width: 46.8%)

The graph of $f (x)$ has already been drawn for your reference. No marks will be awarded for the graph of $f (x)$.

== Solution

#image("assets/2378d5f6-1a56-4f92-937e-09053f24d326-11_985_981_554_242.jpg", width: 46.2%)

1 mark for horizontal reflection

1 mark for absolute value

1 mark for vertical stretch

3 marks

#pagebreak()

= mb-pc40s-2026-jun-q10

== Stem

Solve, algebraically.

$log (x - 1)+ log (x + 2)= 1$

== Solution

$log [(x - 1)(x + 2)] & = 1 \ (x - 1)(x + 2) & = 10 ^(1) \ x ^(2)+ x - 2 & = 10 \ x ^(2)+ x - 12 & = 0 \ (x + 4)(x - 3) & = 0 \ x = - 4 x & = 3$

1 mark for product law

1 mark for exponential form

$frac(1, 2)$ mark for the permissible value of $x$ $frac(1, 2)$ mark for showing the rejection of the extraneous root

#pagebreak()

= mb-pc40s-2026-jun-q11

== Stem

Justify that there are only two negative terms in the expansion of $(- 2 x + 5 y)^(4)$.

== Solution

$upright(t)_(1)= ""_(4) C_(0)(- 2 x)^(4)(5 y)^(0) -> +$

$upright(t)_(2)= ""_(4) C_(1)(- 2 x)^(3)(5 y)^(1) -> -$

$upright(t)_(3)= ""_(4) C_(2)(- 2 x)^(2)(5 y)^(2) -> +$

$upright(t)_(4)= ""_(4) C_(3)(- 2 x)^(1)(5 y)^(3) -> -$

$upright(t)_(5)= ""_(4) C_(4)(- 2 x)^(0)(5 y)^(4) -> +$

The term is negative only when $(- 2 x)$ has an odd exponent, which occurs twice.

1 mark

#pagebreak()

= mb-pc40s-2026-jun-q12

== Stem

The graph of $y = 5 sin (2 x)+ 3$ below can be used to solve the equation $0 = 5 sin (2 x)+ 3$. State how many solutions there are to the equation $0 = 5 sin (2 x)+ 3$ over the interval $[0, 2 pi ]$.

#image("assets/77052c8c-b56e-4088-a63f-96d745fc89b6-12_1370_871_558_638.jpg", width: 41.0%)

== Solution

#image("assets/2378d5f6-1a56-4f92-937e-09053f24d326-14_1378_881_556_638.jpg", width: 41.5%)

There are four solutions.

1 mark

#pagebreak()

= mb-pc40s-2026-jun-q13

== Stem

Given the functions, $f (x)= x ^(2)- 1$ and $g (x)= x + 1$, a) state the equation of $h (x)= frac(f (x), g (x))$.

$h (x)=$

$\_ \_ \_ \_$

b) sketch the graph of $h (x)$.

#image("assets/77052c8c-b56e-4088-a63f-96d745fc89b6-13_912_906_1531_242.jpg", width: 42.6%)

== Solution

a) $h (x)= frac(x ^(2)- 1, x + 1)$

$& = frac((x + 1)(x - 1), (x + 1)) \ & = x - 1 , x != - 1$

b)

#image("assets/2378d5f6-1a56-4f92-937e-09053f24d326-15_931_910_1233_296.jpg", width: 42.8%)

1 mark for shape of graph

consistent with a)

1 mark for point of discontinuity

(hole) at $x = - 1$

2 marks

Note:

Deduct a maximum of 1 mark for the concept error of not restricting domain.

Deduct $frac(1, 2)$ mark for procedural error (not stating domain of simplified function in part a)

if graph shows the correct domain.

#pagebreak()

= mb-pc40s-2026-jun-q14

== Stem

State an equation for $g (x)$, in terms of $f (x)$.

#image("assets/77052c8c-b56e-4088-a63f-96d745fc89b6-14_955_970_474_590.jpg", width: 45.6%)

$g (x)=$

$\_ \_ \_ \_$

== Solution

#image("assets/2378d5f6-1a56-4f92-937e-09053f24d326-16_949_966_485_588.jpg", width: 45.5%)

$g (x)= frac(1, 2) f (x)- 3$

1 mark for vertical compression

1 mark for vertical translation

2 marks

#pagebreak()

= mb-pc40s-2026-jun-q15

== Stem

Sketch the graph of a polynomial function, $p (x)$, with the following characteristics: - degree 5 - leading coefficient of -1 - a zero at -3, with a multiplicity of 3 - a zero at 1, with a multiplicity of 2

#image("assets/77052c8c-b56e-4088-a63f-96d745fc89b6-15_1034_1043_786_554.jpg", width: 49.1%)

== Solution

#image("assets/2378d5f6-1a56-4f92-937e-09053f24d326-17_908_921_852_242.jpg", width: 43.3%)

1 mark for $x$-intercept at -3

with a multiplicity of 3

1 mark for $x$-intercept at 1

with a multiplicity of 2 $frac(1, 2)$ mark for end behaviour $frac(1, 2)$ mark for $y$-intercept

3 marks

#pagebreak()