#set page(paper: "a4", margin: 15mm)

#set text(size: 10pt)

= mb-pc40s-2015-jun

Typst conversion review. OCR content and mathematical accuracy require editorial review.

#pagebreak()

= Question 1

Use the information in the diagram to determine the value of the arc length \" $s $ \"\, given the central

angle of $56 ^(degree )$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jun/assets/2a76f9b0-a716-4787-9d00-4e552fc27afb-01_265_291_502_573.jpg", width: 13.7%)

== Solution

$   & theta = 56 ^(degree ) times  frac(pi ,180 ^(degree )) \  & theta = frac(56  pi ,180 ) " or " frac(14  pi ,45 ) \  & s = theta  r  \  & s = lr(\( frac(14  pi ,45 )\) )\(3  upright(space.nobreak m )\) \  & s = frac(14  pi ,15 ) upright(space.nobreak m ) " or " 2.932  upright(space.nobreak m )   $

1 mark for conversion

1 mark for substitution

2 marks

#pagebreak()

= Question 2

Solve $tan  ^(2 ) theta - 5  tan  theta + 4 = 0 $ where $theta  in  bb(R )$.

== Solution

Method 1

$   & \(tan  theta - 1 \)\(tan  theta - 4 \)= 0  \  & tan  theta = 1  quad  tan  theta = 4  \  & quad  theta _(r )= 1.3258  \  & quad  theta = frac(pi ,4 )\, frac(5  pi ,4 ) quad  theta = 1.326 \,4.467  \  & quad  theta = 0.785 \,3.927    $

1 mark for solving for $tan  theta $ \( $frac(1 ,2 )$ mark for each

branch\)

2 marks \( $frac(1 ,2 )$ mark for each value of $theta $ \)

$  lr( mat(delim: #none,  theta  "" , = frac(pi ,4 )+ 2  k  pi  "" ; "" , = 1.326 + 2  k  pi  "" ; "" , = frac(5  pi ,4 )+ 2  k  pi  "" ; "" , = 4.467 + 2  k  pi  )\} ) " where " k  in  upright(I )  $

1 mark for general solution

4 marks

Method 2

$   &  \(tan  theta - 1 \)\(tan  theta - 4 \) & = 0  \  tan  theta  & = 1  quad  tan  theta  \  quad  theta _(r ) & = 1.3258  \  theta = frac(pi ,4 ) & theta = 1.326  \  theta = 0.785  &    $

1 mark for solving for $tan  theta $ \( $frac(1 ,2 )$ mark for each

branch\)

2 marks \( 1 mark for each value of $theta $ \)

$  lr( mat(delim: #none,  theta  "" , = frac(pi ,4 )+ k  pi  "" ; "" , = 1.326 + k  pi  )\} ) " where " k  in  upright(I )  $

1 mark for general solution

4 marks

#pagebreak()

= Question 3

Solve:

$  2 ^(5  x )= 3 \(5 \)^(x - 3 )  $

== Solution

$  5  x  log  2 = log  3 + \(x - 3 \) log  5   $

$  5  x  log  2 = log  3 + x  log  5 - 3  log  5   $

$  5  x  log  2 - x  log  5 = log  3 - 3  log  5   $

$  x \(5  log  2 - log  5 \)= log  3 - 3  log  5   $

$  x = frac(log  3 - 3  log  5 ,5  log  2 - log  5 )  $

$  x = - 2.009   $

$frac(1 ,2 )$ mark for applying logarithms

1 mark for product rule

1 mark for power rule

$frac(1 ,2 )$ mark for collecting like terms

$frac(1 ,2 )$ mark for isolating $x $

$frac(1 ,2 )$ mark for evaluating a quotient of logarithms

4 marks

#pagebreak()

= Question 4

David and Sarah are in a class of 10 boys and 8 girls.

A committee of 3 boys and 2 girls is to be selected from the students in this class.

Determine the number of possible committees if David and Sarah cannot be on the same

committee.

== Solution

Method 1

#table(stroke: none,
columns: 3,
align: (left, left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2), table.vline(stroke: .5pt, x: 3),
table.hline(stroke: .5pt),
[All: ], [$ "" _(10 ) C _(3 ) times  "" _(8 ) C _(2 )= 3360 $ ], [1 mark for all possible committees ],
table.hline(stroke: .5pt),
[Both: ], [$ "" _(9 ) C _(2 ) times  "" _(7 ) C _(1 )= 252 $ ], [1 mark for both on the committee ],
table.hline(stroke: .5pt),
[], [$3360 - 252 = 3108 $ ], [1 mark for subtraction of cases ],
table.hline(stroke: .5pt),
[], [], [3 marks ],
table.hline(stroke: .5pt),
[],
);

Method 2

#table(stroke: none,
columns: 3,
align: (left, left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2), table.vline(stroke: .5pt, x: 3),
table.hline(stroke: .5pt),
[Case 1: David\, not Sarah ], [$ "" _(9 ) C _(2 ) times  "" _(7 ) C _(2 )= 756 $ ], [$frac(1 ,2 )$ mark for Case 1 ],
table.hline(stroke: .5pt),
[Case 2: Sarah\, not David ], [$ "" _(9 ) C _(3 ) times  "" _(7 ) C _(1 )= 588 $ ], [$frac(1 ,2 )$ mark for Case 2 ],
table.hline(stroke: .5pt),
table.cell(colspan: 2)[Case 3: Neither David nor Sarah $756 + 588 + 1764 = 3108 $ ], [1 mark for Case 3 ],
table.hline(stroke: .5pt),
[], [], [1 mark for addition of cases ],
table.hline(stroke: .5pt),
[], [], [3 marks ],
table.hline(stroke: .5pt),
[],
);

#pagebreak()

= Question 5

In the binomial expansion of $lr(\( frac(3 ,x ^(2 ))- x ^(5 )\) )^(10 )$\, simplify the 7 th term.

== Solution

$   & t _(7 )=  "" _(10 ) C _(6 )lr(\( frac(3 ,x ^(2 ))\) )^(4 )lr(\( - x ^(5 )\) )^(6 ) \  & t _(7 )= 210 lr(\( frac(81 ,x ^(8 ))\) )lr(\( x ^(30 )\) ) \  & t _(7 )= 17010  x ^(22 )   $

2 marks \(1 mark for $ "" _(10 ) C _(6 )\, frac(1 ,2 )$ mark for

each consistent factor\)

1 mark for simplification \( $frac(1 ,2 )$ mark for

coefficient\, $frac(1 ,2 )$ mark for exponent\)

3 marks

#pagebreak()

= Question 6

A lake affected by acid rain has a pH of 4.4.

A person suffering from heartburn has a stomach acid pH of 1.2.

The pH of a solution is defined as $upright(p H )= - log  lr(\[ upright(H )^(+ )\] )$where $lr(\[ upright(H )^(+ )\] )$is the hydrogen ion

concentration.

How many times greater is the hydrogen ion concentration of the stomach than that of the lake?

Express your answer as a whole number.

== Solution

Method 1

$  mat(delim: #none,  upright(p H ) "" , = - log  lr(\[ upright(H )^(+ )\] ) "" , "" ; - upright(p H ) "" , = log  lr(\[ upright(H )^(+ )\] ) "" , "" , "" ; lr(\[ upright(H )^(+ )\] ) "" , = 10 ^(- upright(p H )) "" , "" , 1  " mark for exponential form " "" ; frac(lr(\[ upright(H )^(+ )\] )_("stomach "),lr(\[ upright(H )^(+ )\] )_("lake ")) "" , = frac(10 ^(- 1.2 ),10 ^(- 4.4 )) "" , "" , 1  " mark for comparison " "" ; "" , = 10 ^(3.2 ) "" , "" , "" ; "" , = 1584.9  "" , "" , "" ; "" , = 1585  "" , " marks " )  $

Method 2

Lake

$   4.4  & = - log  lr(\[ upright(H )^(+ )\] ) \  - 4.4  & = log  lr(\[ upright(H )^(+ )\] ) \  10 ^(- 4.4 ) & = lr(\[ upright(H )^(+ )\] )   $

Stomach

$   1.2  & = - log  lr(\[ upright(H )^(+ )\] ) \  - 1.2  & = log  lr(\[ upright(H )^(+ )\] ) \  10 ^(- 1.2 ) & = lr(\[ upright(H )^(+ )\] )   $

$frac(1 ,2 )$ mark for exponential form

$   frac(lr(\[ upright(H )^(+ )\] )_("stomach "),lr(\[ upright(H )^(+ )\] )_("lake ")) & = frac(10 ^(- 1.2 ),10 ^(- 4.4 )) \  & = 10 ^(3.2 ) \  & = 1585    $

1 mark for comparison

2 marks

#pagebreak()

= Question 7

Solve the following equation algebraically over the interval $\[0 \,2  pi \]$.

$  cos  2  theta - 3  sin  theta - 2 = 0   $

== Solution

$  mat(delim: #none,  lr(\( 1 - 2  sin  ^(2 ) theta \) )- 3  sin  theta - 2 = 0  "" ; - 2  sin  ^(2 ) theta - 3  sin  theta - 1 = 0  "" ; 2  sin  ^(2 ) theta + 3  sin  theta + 1 = 0  "" ; \(2  sin  theta + 1 \)\(sin  theta + 1 \)= 0  )  $

$   sin  theta  & = - frac(1 ,2 ) & sin  theta  & = - 1  \  theta  & = frac(7  pi ,6 )\, frac(11  pi ,6 ) & theta  & = frac(3  pi ,2 )   $

1 mark for correct substitution of an appropriate identity

1 mark for solving for $sin  theta $ \( $frac(1 ,2 )$ mark for each branch\)

2 marks for solutions \(1 mark for each branch\; $frac(1 ,2 )$ mark for

each value in the left branch\)

4 marks

#pagebreak()

= Question 8

Explain how the value of $n $ affects the behaviour of the graph of the polynomial function

$p \(x \)= \(x + 3 \)\(x - 1 \)^(n )$\, as $p \(x \)$ approaches the $x $-intercept at $x = 1 $.

== Solution

If $n $ is even\, the graph will turn at the $x $-axis at $x = 1 $.

If $n $ is odd\, the graph will cross the $x $-axis at $x = 1 $.

or

As $n $ increases\, $p \(x \)$ will become flatter around the intercept at $x = 1 $.

#pagebreak()

= Question 9

Sketch the angle $- 320 ^(degree )$ in standard position.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jun/assets/2a76f9b0-a716-4787-9d00-4e552fc27afb-09_866_873_494_526.jpg", width: 41.1%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jun/assets/35fa1966-0f35-485b-af28-2b9c4daf0c0a-09_533_591_636_157.jpg", width: 27.8%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jun/assets/35fa1966-0f35-485b-af28-2b9c4daf0c0a-09_198_651_700_969.jpg", width: 30.6%)

- If directional arrow is not indicated\, it is a communication error\, E1 \(final answer not stated\).

#pagebreak()

= Question 10

Given the graph of $y = f \(x \)$\, explain how to graph $y = f \(- x \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jun/assets/2a76f9b0-a716-4787-9d00-4e552fc27afb-10_656_714_545_348.jpg", width: 33.6%)

== Solution

Multiply the $x $-coordinates by -1 .

or

Reflect the graph over the $y $-axis.

#pagebreak()

= Question 11

Explain how the graph of $y = frac(3 \(x - 1 \),\(x - 1 \))$ is different than the graph of $y = 3 $.

== Solution

There is a point of discontinuity \(hole\) when $x = 1 $ on the graph of $y = frac(3 \(x - 1 \),\(x - 1 \))$. $bold(1 )$ mark

#pagebreak()

= Question 12

Given the graph of $f \(x \)$\, sketch the graph of $g \(x \)= 2  f \(3  x \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jun/assets/2a76f9b0-a716-4787-9d00-4e552fc27afb-12_1778_942_487_457.jpg", width: 44.3%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jun/assets/35fa1966-0f35-485b-af28-2b9c4daf0c0a-12_836_1519_1530_453.jpg", width: 71.5%)

#pagebreak()

= Question 13

Determine the equation of the radical function represented by the graph.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jun/assets/2a76f9b0-a716-4787-9d00-4e552fc27afb-13_639_660_524_425.jpg", width: 31.1%)

== Solution

$y = 2  sqrt(x - 1 )- 2 $

or

1 mark for vertical stretch

1 mark for horizontal translation

1 mark for vertical translation

3 marks

$y = sqrt(4 \(x - 1 \))- 2 $

1 mark for horizontal compression

1 mark for horizontal translation

1 mark for vertical translation

3 marks

#pagebreak()

= Question 14

There are 2 types of pencils\, 3 colours of highlighters\, and 5 styles of pens.

If you must select one of each to form a set\, how many different sets of writing instruments

are possible?

*A.*

10

*B.*

11

*C.*

25

*D.*

30

== Solution

Correct answer: D

30

#pagebreak()

= Question 15

The point $P \(theta \)$ lies on the unit circle. What are the coordinates of the point $P $ if $theta = 120 ^(degree )$ ?

*A.*

$lr(\( - frac(1 ,2 )\, frac(sqrt(3 ),2 )\) )$

*B.*

$lr(\( - frac(sqrt(3 ),2 )\,- frac(1 ,2 )\) )$

*C.*

$lr(\( - frac(sqrt(3 ),2 )\, frac(1 ,2 )\) )$

*D.*

$lr(\( frac(1 ,2 )\, frac(sqrt(3 ),2 )\) )$

== Solution

Correct answer: A

$lr(\( - frac(1 ,2 )\, frac(sqrt(3 ),2 )\) )$

#pagebreak()

= Question 16

Identify the function that has a domain of $\{ x  divides  x  >=  7 \} $ and a range of $\{ y  divides  y  >=  0 \} $.

*A.*

$f \(x \)= sqrt(x )+ 7 $

*B.*

$f \(x \)= sqrt(x )- 7 $

*C.*

$f \(x \)= sqrt(x + 7 )$

*D.*

$f \(x \)= sqrt(x - 7 )$

== Solution

Correct answer: D

$f \(x \)= sqrt(x - 7 )$

#pagebreak()

= Question 17

Using $y = - 10  cos  \[upright(space.nobreak B )\(x - upright(C )\)\]+ upright(D )$\, the value of C that corresponds to the following graph is:

*A.*

5

*B.*

10

*C.*

15

*D.*

20

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jun/assets/ecf0e3eb-61b1-476f-8bf6-d57e6203a18b-02_635_654_1585_782.jpg", width: 30.8%)

== Solution

Correct answer: B

10

#pagebreak()

= Question 18

Given the following row of Pascal's Triangle\, identify the binomial expansion with these

coefficients.

$mat(delim: #none, 1  "" , 5  "" , 10  "" , 10  "" , 5  "" , 1 )$

*A.*

$\(x + y \)^(4 )$

*B.*

$\(x + y \)^(5 )$

*C.*

$\(x + y \)^(6 )$

*D.*

$\(x + y \)^(7 )$

== Solution

Correct answer: B

$\(x + y \)^(5 )$

#pagebreak()

= Question 19

Identify the graph of the function $f \(x \)= - \(x - 2 \)\(x - 1 \)^(2 )\(x + 1 \)$.

*A.*

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jun/assets/ecf0e3eb-61b1-476f-8bf6-d57e6203a18b-03_424_447_1497_348.jpg", width: 21.0%)

*B.*

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jun/assets/ecf0e3eb-61b1-476f-8bf6-d57e6203a18b-03_413_424_1508_1035.jpg", width: 20.0%)

*C.*

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jun/assets/ecf0e3eb-61b1-476f-8bf6-d57e6203a18b-03_407_428_2015_352.jpg", width: 20.1%)

*D.*

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jun/assets/ecf0e3eb-61b1-476f-8bf6-d57e6203a18b-03_394_424_2028_1035.jpg", width: 20.0%)

== Solution

Correct answer: D

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jun/assets/ecf0e3eb-61b1-476f-8bf6-d57e6203a18b-03_394_424_2028_1035.jpg", width: 20.0%)

#pagebreak()

= Question 20

Determine the value of $log  _(9 )lr(\( log  _(3 ) 27 \) )$.

*A.*

$frac(1 ,3 )$

*B.*

$frac(1 ,2 )$

*C.*

2

*D.*

3

== Solution

Correct answer: B

$frac(1 ,2 )$

#pagebreak()

= Question 21

If $\(x \, y \)$ is a point on the graph of $y = f \(x \)$\, identify the coordinates of this point on the graph

of $g \(x \)= f \(2  x \)+ 5 $.

*A.*

$lr(\( frac(x ,2 )\, y + 5 \) )$

*B.*

$\(2  x \, y + 5 \)$

*C.*

$lr(\( frac(x ,2 )\, y - 5 \) )$

*D.*

$lr(\( frac(x ,2 )- 5 \, y \) )$

== Solution

Correct answer: A

$lr(\( frac(x ,2 )\, y + 5 \) )$

#pagebreak()

= Question 22

Identify an equivalent expression for $1 + log  _(2 ) 5 $.

*A.*

$log  _(2 ) 5 $

*B.*

$log  _(2 ) 7 $

*C.*

$log  _(2 ) 10 $

*D.*

$log  _(2 ) 11 $

== Solution

Correct answer: C

$log  _(2 ) 10 $

#pagebreak()

= Question 23

Solve:

$  2  log  _(4 ) x - log  _(4 )\(x + 3 \)= 1   $

== Solution

$   2  log  _(4 ) x - log  _(4 )\(x + 3 \) & = 1  \  log  _(4 )lr(\( frac(x ^(2 ),x + 3 )\) ) & = 1  \  4 ^(1 ) & = frac(x ^(2 ),x + 3 ) \  4  x + 12  & = x ^(2 ) \  x ^(2 )- 4  x - 12  & = 0  \  \(x - 6 \)\(x + 2 \) & = 0  \  x = 6  quad  x > - 2  &   $

1 mark for power rule

1 mark for quotient rule

1 mark for exponential form

$frac(1 ,2 )$ mark for solving for $x $

$frac(1 ,2 )$ mark for rejecting extraneous root

4 marks

#pagebreak()

= Question 24

The following transformations are applied to $f \(x \)$\, resulting in a new function\, $g \(x \)$.

- reflection over the $y $-axis

- horizontal translation of 3 units to the right

- vertical translation of 4 units down

Write the equation of $g \(x \)$ in terms of $f \(x \)$.

$  g \(x \)=   $

== Solution

$  g \(x \)= f \(- \(x - 3 \)\)- 4   $

or

1 mark for horizontal shift

1 mark for vertical shift

1 mark for reflection

3 marks

$  g \(x \)= f \(- x + 3 \)- 4   $

#pagebreak()

= Question 25

a\) 3 marks

b\) 1 mark

116 117

The height of a bicycle pedal as the bicycle is moving at a constant speed can be represented by

the following function:

$  h \(t \)= 15  cos  frac(2  pi ,5 ) t + 30   $

where $h $ is the height of the pedal above the ground\, in cm \, and $t $ is the time\, in seconds.

a\) Sketch a graph of at least one period of this function\, where $t  >=  0 $.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jun/assets/ecf0e3eb-61b1-476f-8bf6-d57e6203a18b-08_869_862_803_638.jpg", width: 40.6%)

b\) Determine the height of the bicycle pedal at 7.5 seconds.

== Solution

- \[\]

  #image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jun/assets/35fa1966-0f35-485b-af28-2b9c4daf0c0a-20_741_1519_932_183.jpg", width: 71.5%)

  b\) From the graph:

  $  h \(t \)= 15  upright(space.nobreak c m )  $

  or

  From the equation:

  $   h \(t \) & = 15  cos  frac(2  pi ,5 )\(7.5 \)+ 30  \  & = 15  cos  3  pi + 30  \  & = 15 \(- 1 \)+ 30  \  & = 15  upright(space.nobreak c m )   $

#pagebreak()

= Question 26

Sketch the graph of the function $f \(x \)$ and determine the $y $-intercept.

$  f \(x \)= frac(4 ,\(x - 2 \)\(x + 2 \))  $

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jun/assets/ecf0e3eb-61b1-476f-8bf6-d57e6203a18b-09_869_873_640_586.jpg", width: 41.1%)

$y $-intercept:

$\_ \_ \_ \_ $

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jun/assets/35fa1966-0f35-485b-af28-2b9c4daf0c0a-21_776_930_733_161.jpg", width: 43.8%)

$\_ \_ \_ \_ $

-1

$frac(1 ,2 )$ mark for $y $-intercept

4 marks

#pagebreak()

= Question 27

Kim solved the following logarithmic equation:

$   log  _(2 )lr(\( - frac(x ,3 )\) )= log  _(2 )\(x - 4 \) \  - frac(x ,3 )= x - 4  \  - x = 3  x - 12  \  - 4  x = - 12  \  x  <=  3    $

Explain why $x = 3 $ is an extraneous solution.

== Solution

$x = 3 $ is an extraneous solution because the argument in a logarithmic

equation cannot be negative.

#pagebreak()

= Question 28

Determine the equation of the polynomial function represented by the graph.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jun/assets/ecf0e3eb-61b1-476f-8bf6-d57e6203a18b-11_789_839_481_403.jpg", width: 39.5%)

$p \(x \)= $

== Solution

$   p \(x \) & = a \(x - 2 \)^(2 )\(x + 3 \) \  24  & = a \(0 - 2 \)^(2 )\(0 + 3 \) \  24  & = a \(4 \)\(3 \) \  24  & = 12  a  \  a  & = 2    $

$  p \(x \)= 2 \(x - 2 \)^(2 )\(x + 3 \)  $

1 mark for $x $-intercepts \( $frac(1 ,2 )$ mark for each\)

1 mark for multiplicity at $x = 2 $

1 mark for leading coefficient

3 marks

#pagebreak()

= Question 29

Determine the coterminal angles with $frac(2  pi ,3 )$ over the interval $\[- 2  pi \, 4  pi \]$.

== Solution

$  - frac(4  pi ,3 )\, frac(8  pi ,3 ) quad  1  " mark ( " 1  \/ 2  " mark for each coterminal angle) "  $

1 mark

#pagebreak()

= Question 30

a\) Solve the following equation:

$  0 = sqrt(4  x - 8 )- 2   $

b\) Explain how your answer in a\) is related to the graph of $y = sqrt(4  x - 8 )- 2 $.

== Solution

a\)

$   4  & = 4  x - 8  \  12  & = 4  x  \  x  & = 3 \, x  >=  2    $

b\) The answer in a\) is the $x $-intercept of the graph.

- $x  >=  2 $ does not need to be shown.

#pagebreak()

= Question 31

Determine the exact value of $sin  frac(13  pi ,12 )$.

== Solution

$   sin  frac(13  pi ,12 ) & = sin  lr(\( frac(3  pi ,4 )+ frac(pi ,3 )\) ) \  & = lr(\( sin  frac(3  pi ,4 )\) )lr(\( cos  frac(pi ,3 )\) )+ lr(\( cos  frac(3  pi ,4 )\) )lr(\( sin  frac(pi ,3 )\) ) \  & = lr(\( frac(sqrt(2 ),2 )\) )lr(\( frac(1 ,2 )\) )+ lr(\( - frac(sqrt(2 ),2 )\) )lr(\( frac(sqrt(3 ),2 )\) ) \  & = frac(sqrt(2 )- sqrt(6 ),4 )   $

1 mark for combination

2 marks for exact values \( $frac(1 ,2 )$ mark for each\)

3 marks

- Other combinations are possible.

#pagebreak()

= Question 32

a\) 2 marks

b\) 1 mark

Given the functions $f \(x \)= x + 2 $ and $g \(x \)= frac(1 ,x - 5 )$ :

a\) Determine the equation of the composite function $f \(g \(x \)\)$ and its domain.

$  f \(g \(x \)\)=   $

$\_ \_ \_ \_ $

domain:

$\_ \_ \_ \_ $

b\) Determine the $x $-intercept and $y $-intercept of $f \(g \(x \)\)$.

$x $-intercept:

$\_ \_ \_ \_ $

$y $-intercept:

$\_ \_ \_ \_ $

== Solution

a\) $quad  f \(g \(x \)\)= frac(1 ,x - 5 )+ 2 $

or

$f \(g \(x \)\)= frac(2  x - 9 ,x - 5 )$

domain: $\{ x  in  bb(R )\, x  !=  5 \} $

b\) $x $-intercept:

$frac(9 ,2 )$

$\_ \_ \_ \_ $

$frac(1 ,2 )$ mark for $x $-intercept

$y $-intercept:

$frac(9 ,5 )$

$\_ \_ \_ \_ $

$frac(1 ,2 )$ mark for $y $-intercept

1 mark

#pagebreak()

= Question 33

a\) Sketch the graph of $f \(x \)= log  _(5 )\(x - 1 \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jun/assets/ecf0e3eb-61b1-476f-8bf6-d57e6203a18b-16_872_877_491_526.jpg", width: 41.3%)

b\) Sketch the graph of $f ^(- 1 )\(x \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jun/assets/ecf0e3eb-61b1-476f-8bf6-d57e6203a18b-16_867_866_1570_537.jpg", width: 40.8%)

== Solution

b\)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jun/assets/35fa1966-0f35-485b-af28-2b9c4daf0c0a-28_816_859_683_178.jpg", width: 40.4%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jun/assets/35fa1966-0f35-485b-af28-2b9c4daf0c0a-28_812_853_1581_187.jpg", width: 40.1%)

$frac(1 ,2 )$ mark for vertical asymptote at $x = 1 $

$frac(1 ,2 )$ mark for $x $-intercept at $x = 2 $

$frac(1 ,2 )$ mark for increasing logarithmic function

$frac(1 ,2 )$ mark for consistent point on the

logarithmic graph

2 marks

1 mark for the graph of the inverse

function consistent with a\)

1 mark

#pagebreak()

= Question 34

Explain what the graph of a rational function looks like near a vertical asymptote.

== Solution

The graph approaches infinity \(positive or negative\) as it approaches the asymptote.

or

The graph approaches the asymptote\, but does not touch it.

#pagebreak()

= Question 35

Given the graph of $f \(x \)= \(x - 2 \)^(2 )$\,

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jun/assets/ecf0e3eb-61b1-476f-8bf6-d57e6203a18b-17_628_656_1465_262.jpg", width: 30.9%)

determine one possible restriction for the domain of $f \(x \)$ so that its inverse is a function.

Domain:

$\_ \_ \_ \_ $

== Solution

$\_ \_ \_ \_ $

$\[2 \, oo \)$

$\_ \_ \_ \_ $

$\[2 \, oo \)$

$\_ \_ \_ \_ $

Domain:

$\_ \_ \_ \_ $

$\(- oo \, 2 \)$

$\_ \_ \_ \_ $

$\_ \_ \_ \_ $

- Other solutions are possible.

#pagebreak()

= Question 36

Over the interval $\[0 \,2  pi \]$\, determine the non-permissible values of $theta $ in the expression

$csc  theta \(cos  theta + 1 \)$.

== Solution

$csc  theta = frac(1 ,sin  theta )$

$sin  theta  !=  0 $

$  theta = 0 \, pi \, 2  pi   $

1 mark for correct substitution of an appropriate identity

$frac(1 ,2 )$ mark for $sin  theta  !=  0 $

$frac(1 ,2 )$ mark for consistent non-permissible values

2 marks

#pagebreak()

= Question 37

Explain why $ "" _(3 ) C _(8 )$ is undefined.

== Solution

In the formula $ "" _(n ) C _(r )$\, the number of objects\, $n $\, must be larger than

or equal to the number of objects selected\, $r $.

or

You can't select 8 objects from a total of 3.

#pagebreak()

= Question 38

Solve:

$   "" _(n ) P _(3 )= 48 \(n - 1 \)  $

== Solution

#table(stroke: none,
columns: 1,
align: (left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1),
table.hline(stroke: .5pt),
[$frac(n ! ,\(n - 3 \)! )= 48 \(n - 1 \)$ ],
table.hline(stroke: .5pt),
[$frac(\(n \)\(n - 1 \)\(n - 2 \)\(n - 3 \)! ,\(n - 3 \)! )= 48 \(n - 1 \)$ ],
table.hline(stroke: .5pt),
[$n \(n - 2 \)= 48 $ ],
table.hline(stroke: .5pt),
[$n ^(2 )- 2  n - 48 = 0 $ ],
table.hline(stroke: .5pt),
[$\(n - 8 \)\(n + 6 \)= 0 $ ],
table.hline(stroke: .5pt),
[$n = 8  quad  n > - 6 $ ],
table.hline(stroke: .5pt),
[],
);

$frac(1 ,2 )$ mark for substitution in correct formula

1 mark for expansion of factorial

$frac(1 ,2 )$ mark for simplification of factorials

$frac(1 ,2 )$ mark for solving for both values of $n $

$frac(1 ,2 )$ mark for rejecting extraneous solution

3 marks

#pagebreak()

= Question 39

b\) 1 mark

c\) 1 mark

Christine dives off a diving board.

Her dive is modelled by the function $h \(t \)= t ^(3 )- 3  t ^(2 )- t + 3 $\, where $h $ is her height in metres\,

relative to the water surface and $t $ is the time in seconds after diving off the diving board.

a\) Given that $\(t + 1 \)$ is a factor for the function $h \(t \)$\, determine the other factors.

b\) Sketch the graph of the function $h \(t \)$ for the time interval $t = 0 $ to $t = 3 $.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jun/assets/ecf0e3eb-61b1-476f-8bf6-d57e6203a18b-21_645_626_1450_502.jpg", width: 29.5%)

c\) Determine how many seconds Christine is underwater.

== Solution

a\)

#table(stroke: none,
columns: 5,
align: (left, left, left, left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2), table.vline(stroke: .5pt, x: 3), table.vline(stroke: .5pt, x: 4), table.vline(stroke: .5pt, x: 5),
table.hline(stroke: .5pt),
[-1 ], [1 ], [-3 ], [-1 ], [3 ],
table.hline(stroke: .5pt),
[↓ ], [], [-1 ], [4 ], [-3 ],
table.hline(stroke: .5pt),
[1 ], [], [-4 ], [3 ], [0 ],
table.hline(stroke: .5pt),
[$h \(t \)$ ], [], [$\(t + 1 \)$ ], [\) $lr(\( t ^(2 ) )$ ], [$- 4  t + 3 \)$ ],
table.hline(stroke: .5pt),
[$h \(t \)$ ], [], [$\(t + 1 \)$ ], [\)\( $t $ ], [1\) $\(t - 3 \)$ ],
table.hline(stroke: .5pt),
[],
);

b\)

c\) Christine is underwater for 2 seconds.

$frac(1 ,2 )$ mark for $t = - 1 $

1 mark for synthetic division \(or equivalent strategy\)

$frac(1 ,2 )$ mark for determining other factors

2 marks

$frac(1 ,2 )$ mark for $t $-intercepts

$frac(1 ,2 )$ mark for $h $-intercept

1 mark

1 mark

#pagebreak()

= Question 40

Prove the identity for all permissible values of $x $.

$  sec  x + tan  x = frac(cos  x ,1 - sin  x )  $

#table(stroke: none,
columns: 2,
align: (left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2),
table.hline(stroke: .5pt),
[Left-Hand Side ], [Right-Hand Side ],
table.hline(stroke: .5pt),
[],
);

== Solution

#table(stroke: none,
columns: 3,
align: (left, left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2), table.vline(stroke: .5pt, x: 3),
table.hline(stroke: .5pt),
[Method 1 ], [], [],
table.hline(stroke: .5pt),
[], [Left-Hand Side ], [Right-Hand Side ],
table.hline(stroke: .5pt),
[], [$   & frac(sec  x + tan  x ,cos  x )+ frac(sin  x ,cos  x ) \  & frac(\(1 + sin  x \)\(1 - sin  x \),cos  x \(1 - sin  x \)) \  & frac(1 - sin  ^(2 ) x ,\(1 - sin  x \) cos  x ) \  & frac(cos  ^(2 ) x ,\(1 - sin  x \) cos  x ) \  & frac(cos  x ,1 - sin  x )   $ ], [#table(stroke: none,
columns: 1,
align: (left, ),

[1 mark for correct substitution of appropriate identities ],
[1 mark for logical process to prove the identity ],
[1 mark for algebraic strategies ],
[3 marks ],
); ],
table.hline(stroke: .5pt),
[],
);

#pagebreak()

= Question 41

Given the graph of $f \(x \)$\, sketch the graph of the function $g \(x \)= - | f \(x \)| $.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jun/assets/ecf0e3eb-61b1-476f-8bf6-d57e6203a18b-23_1658_862_499_371.jpg", width: 40.6%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jun/assets/35fa1966-0f35-485b-af28-2b9c4daf0c0a-37_748_866_1427_337.jpg", width: 40.8%)

1 mark for absolute value

1 mark for vertical reflection

2 marks

#pagebreak()

= Question 42

Given that $cot  theta = - frac(2 ,5 )$\, where $theta $ is in Quadrant IV\, determine the exact value of $sin  theta $.

== Solution

$  mat(delim: #none,  quad  P \(2 \,- 5 \) "" , "" , "" ; r ^(2 ) "" , = \(2 \)^(2 )+ \(- 5 \)^(2 ) "" , "" ; r ^(2 ) "" , = 4 + 25  "" , frac(1 ,2 ) " mark for substitution of " x = 2 \, y = - 5  "" ; r  "" , = sqrt(29 ) "" , 1  " mark for " sin  theta lr(\( frac(1 ,2 ) " mark for quadrant, " 1  \/ 2  " mark for value "\) ) )  $

2 marks