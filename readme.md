# NPA Hierarchy
This repos contains a simple code that build a moment matrix for a given degree, number of Alice inputs and number of Bob inputs.

For exemple, this snippet print a the moment matrix $\Gamma$ of degree 2, for 2 Alice and Bob inputs, and all constraints of the type $\Gamma_{i,j}=\Gamma_{i',j'}$.

```python
N, M, d = 2, 2, 2
moment_matrix = MomentMatrix(N, M, d)
print(moment_matrix)
print(moment_matrix.get_constraints())
```
__Results :__
```python
''    I     A0    A1      B0      B1      A1A0      A0B0        A0B1        A0A1        A1B0        A1B1        B1B0        B0B1        
I     1     <A0>  <A1>    <B0>    <B1>    <A1A0>    <A0B0>      <A0B1>      <A0A1>      <A1B0>      <A1B1>      <B1B0>      <B0B1>      
A0    None  1     <A0A1>  <A0B0>  <A0B1>  <A0A1A0>  <B0>        <B1>        <A1>        <A0A1B0>    <A0A1B1>    <A0B1B0>    <A0B0B1>    
A1    None  None  1       <A1B0>  <A1B1>  <A0>      <A1A0B0>    <A1A0B1>    <A1A0A1>    <B0>        <B1>        <A1B1B0>    <A1B0B1>    
B0    None  None  None    1       <B0B1>  <A1A0B0>  <A0>        <A0B0B1>    <A0A1B0>    <A1>        <A1B0B1>    <B0B1B0>    <B1>        
B1    None  None  None    None    1       <A1A0B1>  <A0B1B0>    <A0>        <A0A1B1>    <A1B1B0>    <A1>        <B0>        <B1B0B1>    
A0A1  None  None  None    None    None    1         <A0A1A0B0>  <A0A1A0B1>  <A0A1A0A1>  <A0B0>      <A0B1>      <A0A1B1B0>  <A0A1B0B1>  
A0B0  None  None  None    None    None    None      1           <B0B1>      <A1B0>      <A0A1>      <A0A1B0B1>  <A0B0B1B0>  <A0B1>      
A0B1  None  None  None    None    None    None      None        1           <A1B1>      <A0A1B1B0>  <A0A1>      <A0B0>      <A0B1B0B1>  
A1A0  None  None  None    None    None    None      None        None        1           <A1A0A1B0>  <A1A0A1B1>  <A1A0B1B0>  <A1A0B0B1>  
A1B0  None  None  None    None    None    None      None        None        None        1           <B0B1>      <A1B0B1B0>  <A1B1>      
A1B1  None  None  None    None    None    None      None        None        None        None        1           <A1B0>      <A1B1B0B1>  
B0B1  None  None  None    None    None    None      None        None        None        None        None        1           <B0B1B0B1>  
B1B0  None  None  None    None    None    None      None        None        None        None        None        None        1           

{
    '<A0>': [(2, 1), (6, 3), (7, 4), (8, 5)], 
    '<A1>': [(3, 1), (9, 2), (10, 4), (11, 5)], 
    '<B0>': [(4, 1), (7, 2), (10, 3), (12, 5)], 
    '<B1>': [(5, 1), (8, 2), (11, 3), (13, 4)], 
    '<A0B0>': [(7, 1), (4, 2), (10, 6), (12, 8)], 
    '<A0B1>': [(8, 1), (5, 2), (11, 6), (13, 7)], 
    '<A0A1>': [(9, 1), (3, 2), (10, 7), (11, 8)], 
    '<A1B0>': [(10, 1), (4, 3), (9, 7), (12, 11)], 
    '<A1B1>': [(11, 1), (5, 3), (9, 8), (13, 10)], 
    '<B0B1>': [(13, 1), (5, 4), (8, 7), (11, 10)], 
    '<A0A1B0>': [(10, 2), (9, 4)], 
    '<A0A1B1>': [(11, 2), (9, 5)], 
    '<A0B1B0>': [(12, 2), (7, 5)], 
    '<A0B0B1>': [(13, 2), (8, 4)], 
    '<A1A0B0>': [(7, 3), (6, 4)], 
    '<A1A0B1>': [(8, 3), (6, 5)], 
    '<A1B1B0>': [(12, 3), (10, 5)], 
    '<A1B0B1>': [(13, 3), (11, 4)], 
    '<A0A1B1B0>': [(12, 6), (10, 8)], 
    '<A0A1B0B1>': [(13, 6), (11, 7)]
}
```
A constraint should be read like : `'<A0A1B0>': [(10, 2), (9, 4)],` $\equiv \Gamma_{10,2}=\Gamma_{9,4}$