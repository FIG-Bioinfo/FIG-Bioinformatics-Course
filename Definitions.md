# Basic Definitions

The following set of terms represents simplified
descriptions of a subset of concepts used by biologists
and bioinformaticians.  
In this course, we will very loosely view cells as a
collection or "bag" of abstract "molecular machines".

---

**DNA sequence**: A string in the 4-character alphabet
{a, c, g, t}.  
DNA sequences are normally written in lowercase, but
sometimes uppercase is used to highlight a subsequence.  
Sequences are often referred to indirectly by an
associated identifier.

---

**Contig**: A DNA sequence.

---

**DNA_K_mer**: A DNA sequence of length K  
(e.g., a DNA_20_mer is a DNA sequence of length 20).

A DNA_K_mer X is said to occur in contig Y if X is a
substring of Y.

A DNA_K_mer X is said to occur in sample Y if X occurs
in a contig contained in Y.

---

Let S1 and S2 be two sets.  
Let I be the set of members that occur in both S1 and S2
(i.e., in the intersection of S1 and S2).  
Let U be the union of S1 and S2. Then the **Jaccard
similarity** between sets S1 and S2 is defined as
size(I)/size(U).  

One particular instance of a Jaccard similarity would be
the similarity computed using the sets of DNA_20_mers
contained within two sets of sequences S1 and S2.

---

**Genome**: A set of contigs.

---

**Sample**: A set of contigs that may contain more than
one genome.

---

**Gene**: A named subsequence of a contig that has been
assigned a role.

---

**Role**: An "atomic concept" that describes what a gene
does.

---

A gene's **function** consists of one or more roles.

---

A role R is said to be **singly occurring** in genome G
if exactly one gene in G implements R.

---

A role is said to be **Universal** if it can be expected
to occur in every genome.

---

A role that is both singly-occurring and universal is
called a **Singly-Occurring Universal Role** (abbreviated
as **SOUR**).

---

## Representative Sets

Let U be the Universe of genomes being considered.  
Let there be some measure of similarity between two
genomes.  

Then a set of **Representative Genomes** (or **RepGen
set** for short) is a subset of U such that:

- No two members of the RepGen set are more similar than
  some threshold similarity **Sim**.
- Every member of U is similar to at least one member of
  the RepGen set.

There are several algorithms for building RepGen sets.  
In this course, we will be using the "Stingy Addition"
algorithm.  

### Pseudocode for "Stingy Addition":

```plaintext
RepGenSet = ()   # The "empty list"
ToCheck   = U    # The "Universe of Genomes"
Foreach G1 in ToCheck:
  If no G in RepGenSet is more similar to G1 than Sim:
    Add G1 to RepGenSet
        	
Return RepGenSet
```