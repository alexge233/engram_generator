"""Wikipedia-sourced knowledge atoms."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom

register_atom(Atom(
    atom_type="formula",
    name="mean",
    content="""In mathematics and statistics, the arithmetic mean (   arr-ith-MET-ik), arithmetic average, or just the mean or average is the sum of a collection of numbers divided by the count of numbers in the collection. The collection is often a set of results from an experiment, an observational study, or a survey. The term "arithmetic mean" is preferred in some contexts in mathematics and statistics because it helps to distinguish it from other types of means, such as geometric and harmonic.
Arithmetic means are also frequently used in economics, anthropology, history, and almost every other academic field to some extent. For example, per capita income is the arithmetic average of the income of a nation's population.
While the arithmetic mean is often used to report central tendencies, it is not a robust statistic: it is greatly influenced by outliers (values much larger or smaller than most others). For skewed distributions, such as the distribution of income for which a few people's incomes are substantially higher than most people's, the arithmetic mean may not coincide with one's notion of "middle". In that case, robust statistics, such as the median, may provide a better description of central tendency.


== Definition ==

The arithmetic mean of a set of observed data is equal to the sum of the numerical values of each observation, divided by the total number of observations. Symbolically, for a data set consisting of the values 
  
    
      
        
          x
          
            1
          
        
        ,
        …
        ,
        
          x
          
            n
          
        
      
    
    {\\displaystyle x_{1},\\dots ,x_{n}}
  
, the arithmetic mean is defined by the formula:

  
    
      
        
          x
        
        =
        
          
            1
            n
          
        
        
          (
          
            
              ∑
              
                i
                =
                1
              
              
                n
              
            
            
              
                x
                
                  i
                
              
            
          
          )
        
        =
        
          
            
              
                x
                
                  1
                
              
              +
              
                x
                
                  2
                
              
              +
              ⋯
              +
              
                x
                
                  n
                
              
            
            n
          
        
      
    
    {\\displaystyle {x}={\\frac {1}{n}}\\left(\\sum _{i=1}^{n}{x_{i}}\\right)={\\frac {x_{1}+x_{2}+\\dots +x_{n}}{n}}}
  

In simpler terms, the formula for the arithmetic mean is:

  
    
      
        
          
            Sum of all values
            Number of values
          
        
      
    
    {\\displaystyle {\\frac {\\text{Sum of all values}}{\\text{Number of values}}}}
  

For example, if the monthly salaries of 
  
    
      
        5
      
    
    {\\displaystyle 5}
  
 employees are 
  
    
      
        {
        2500
        ,
        2700
        ,
        2300
        ,
        2650
        ,
        2450
        }
      
    
    {\\displaystyle \\{2500,2700,2300,2650,2450\\}}
  
, then the arithmetic mean is:

  
    
      
        
          
            
              2500
              +
              2700
              +
              2300
              +
              2650
              +
              2450
            
            5
          
        
        =
        2520
      
    
    {\\displaystyle {\\frac {2500+2700+2300+2650+2450}{5}}=2520}
  

If the data set is a statistical population (i.e. consists of every possible observation and not just a subset of them), then the mean of that population is called the population mean and denoted by the Greek letter 
  
    
      
        μ
      
    
    {\\displaystyle \\mu }
  
. If the data set is a statistical sample (a subset of the population), it is called the sample mean (which for a data set 
  
    
      
        X
      
    
    {\\displaystyle X}
  
 is denoted as 
  
    
      
        
          
            X
            ¯
          
        
      
    
    {\\displaystyle {\\overline {X}}}
  
).
The arithmetic mean can be similarly defined for vectors in multiple dimensions, not only scalar values; this is often referred to as a centroid. More generally, because the arithmetic mean is a convex combination (meaning its coefficients sum to 
  
    
      
        1
      
    
    {\\displaystyle 1}
  
), it can be defined on a convex space, not only a vector space.


== History ==
Statistician Churchill Eisenhart, senior researcher fellow at the U. S. National Bureau of Standards, traced the history of the arithmetic mean in detail. In the modern age, it started to be used as a way of combining various observations that should be identical, but were not such as estimates of the direction of magnetic north. In 1635, mathematician Henry Gellibrand described as "meane" the midpoint of a lowest and highest number, not quite the arithmetic mean. In 1668, a person known as "D. B." was quoted in the Transactions of the Royal Society describing "taking the mean" of five values:

In this Table, he [Capt. Sturmy] notes the greatest difference to be 14 minutes; and so taking the mean for the true Variation, he concludes it then and there to be just 1. deg. 27. min.


== Motivating properties ==
The arithmetic mean has several properties that make it interesting, especially as a measure of central tendency. These include:

If numbers 
  
    
      
        
          x
          
            1
          
        
        ,
        …
        ,
        
          x
          
            n
          
        
      
    
    {\\displaystyle x_{1},\\dotsc ,x_{n}}
  
 have a mean 
  
    
      
        
          
            
              x
              ¯
            
          
        
      
    
    {\\displaystyle {\\bar {x}}}
  
, then 
  
    
      
        (
        
          x
          
            1
          
        
        −
        
          
            
              x
              ¯
            
          
        
        )
        +
        ⋯
        +
        (
        
          x
          
            n
          
        
        −
        
          
            
              x
              ¯
            
          
        
        )
        =
        0
      
    
    {\\displaystyle (x_{1}-{\\bar {x}})+\\dotsb +(x_{n}-{\\bar {x}})=0}
  
. Since 
  
    
      
        
          x
          
            i
          
        
        −
        
          
            
              x
              ¯
            
          
        
      
    
    {\\displaystyle x_{i}-{\\bar {x}}}
  
 is the distance from a given number to the mean, one way to interpret this property is by saying that the numbers to the left of the mean are balanced by the numbers to the right. The mean is the only number for which the residuals (deviations from the estimate) sum to zero.""",
    tier=2,
    domain="statistics",
    source="Wikipedia, 'Arithmetic mean'",
    source_url="https://en.wikipedia.org/wiki/Arithmetic_mean",
))

register_atom(Atom(
    atom_type="definition",
    name="median",
    content="""The median of a set of numbers is the value separating the higher half from the lower half of a data sample, a population, or a probability distribution. For a data set, it may be thought of as the "middle" value. The basic feature of the median in describing data compared to the mean (often simply described as the "average") is that it is not skewed by a small proportion of extreme values, and therefore provides a better representation of the center. Median income, for example, may be a better way to describe the center of the income distribution because increases in the largest incomes alone have no effect on the median. For this reason, the median is of central importance in robust statistics.
Median is a 2-quantile; it is the value that partitions a set into two equal parts.


== Finite set of numbers ==
The median of a finite list of numbers is the "middle" number, when those numbers are listed in order from smallest to greatest.
If the data set has an odd number of observations, the middle one is selected (after arranging in ascending order). For example, the following list of seven numbers,

has the median of 6, which is the fourth value.
If the data set has an even number of observations, there is no distinct middle value and the median is usually defined to be the arithmetic mean of the two middle values. For example, this data set of 8 numbers

has a median value of 4.5, that is 
  
    
      
        (
        4
        +
        5
        )
        
          /
        
        2
      
    
    {\\displaystyle (4+5)/2}
  
. (In more technical terms, this interprets the median as the fully trimmed mid-range).
In general, with this convention, the median can be defined as follows: For a data set 
  
    
      
        x
      
    
    {\\displaystyle x}
  
 of 
  
    
      
        n
      
    
    {\\displaystyle n}
  
 elements, ordered from smallest to greatest,


== Definition and notation ==
Formally, a median of a population is any value such that at least half of the population is less than or equal to the proposed median and at least half is greater than or equal to the proposed median. As seen above, medians may not be unique. If each set contains more than half the population, then some of the population is exactly equal to the unique median.
The median is well-defined for any ordered (one-dimensional) data and is independent of any distance metric. The median can thus be applied to student grades that are ranked but not numerical (e.g. working out a median grade when student test scores are graded from F to A). The result might be halfway between grades if there is an even number of students; for an odd number students, one specific grade is determined as the median.
A geometric median, on the other hand, is defined in any number of dimensions. A related concept, in which the outcome is forced to correspond to a member of the sample, is the medoid.
There is no widely accepted standard notation for the median, but some authors represent the median of a variable x as med(x), x͂, as μ1/2, or as M. In any of these cases, the use of these or other symbols for the median needs to be explicitly defined when they are introduced.
The median is a special case of other ways of summarizing the typical values associated with a statistical distribution: it is the 2nd quartile, 5th decile, and 50th percentile.


== Uses ==
The median can be used as a measure of location when one attaches reduced importance to extreme values, typically because a distribution is skewed, extreme values are not known, or outliers are untrustworthy, i.e., may be measurement or transcription errors.
For example, consider the multiset

The median is 2 in this case, as is the mode, and it might be seen as a better indication of the center than the arithmetic mean of 4, which is larger than all but one of the values.  However, the widely cited empirical relationship that the mean is shifted "further into the tail" of a distribution than the median is not generally true.  At most, one can say that the two statistics cannot be "too far" apart; see § Inequality relating means and medians below.
As a median is based on the middle data in a set, it is not necessary to know the value of extreme results in order to calculate it. For example, in a psychology test investigating the time needed to solve a problem, if a small number of people failed to solve the problem at all in the given time a median can still be calculated.
Because the median is simple to understand and easy to calculate, while also a robust approximation to the mean, the median is a popular summary statistic in descriptive statistics.  In this context, there are several choices for a measure of variability: the range, the interquartile range, the mean absolute deviation, and the median absolute deviation.
For practical purposes, different measures of location and dispersion are often compared on the basis of how well the corresponding population values can be estimated from a sample of data. The median, estimated using the sample median, has good properties in this regard. While it is not usually optimal if a given population distribution is assumed, its properties are always reasonably good. For example, a comparison of the efficiency of candidate estimators shows that the sample mean is more statistically efficient when—and only when— data is uncontaminated by data from heavy-tailed distributions or from mixtures of distributions.  Even then, the median has a 64% efficiency compared to the minimum-variance mean (for large normal samples), which is to say the variance of the median will be ~50% greater than the variance of the mean.


== Probability distributions ==
A median of a real-valued random variable 
  
    
      
        X
      
    
    {\\displaystyle X}
  
 is a real number 
  
    
      
        m
      
    
    {\\displaystyle m}
  
 that satisfies 

  
    
      
        P
        ⁡
        (
        X
        <
        m
        )
        ≤
        
          
            1
            2
          
        
        
        
          and
        
        
        P
        ⁡
        (
        X
        >
        m
        )
        ≤
        
          
            1
            2
          
        
      
    
    {\\displaystyle \\operatorname {P} (X<m)\\leq {\\frac {1}{2}}\\quad {\\text{and}}\\quad \\operatorname {P} (X>m)\\leq {\\frac {1}{2}}}
  

or, equivalently with the complementary events,

  
    
      
        P
        ⁡
        (
        X
        ≥
        m
        )
        ≥
        
          
            1
            2
          
        
        
        
          and
        
        
        P
        ⁡
        (
        X
        ≤
        m
        )
        ≥
        
          
            1
            2
          
        
        
        .
      
    
    {\\displaystyle \\operatorname {P} (X\\geq m)\\geq {\\frac {1}{2}}\\quad {\\text{and}}\\quad \\operatorname {P} (X\\leq m)\\geq {\\frac {1}{2}}\\,.}
  

Such an 
  
    
      
        m
      
    
    {\\displaystyle m}
  
 always exists, but needs not be uniquely determined. An equivalent phrasing uses the cumulative distribution function 
  
    
      
        F
        :
        
        
          R
        
        →
        
          R
        
      
    
    {\\displaystyle F\\colon \\,\\mathbb {R} \\to \\mathbb {R} }
  
 of 
  
    
      
        X
        :
      
    
    {\\displaystyle X\\colon }
  

  
    
      
        
          lim
          
            x
            →
            m
            −
          
        
        F
        (
        x
        )
        ≤
        
          
            1
            2
          
        
        ≤
        F
        (
        m
        )
      
    
    {\\displaystyle \\lim _{x\\to m-}F(x)\\leq {\\frac {1}{2}}\\leq F(m)}
  

(cf.""",
    tier=2,
    domain="statistics",
    source="Wikipedia, 'Median'",
    source_url="https://en.wikipedia.org/wiki/Median",
))

register_atom(Atom(
    atom_type="definition",
    name="mode",
    content="""In statistics, the mode is the value that appears most often in a set of data values. If X is a discrete random variable, the mode is the value x at which the probability mass function P(X) takes its maximum value, i.e., x = argmaxxi P(X = xi). In other words, it is the value that is most likely to be sampled.
Like the statistical mean and median, the mode is a summary statistic about the central tendency of a random variable or a population. The numerical value of the mode is the same as that of the mean and median in a normal distribution, but it may be very different in highly skewed distributions.
The mode is not necessarily unique in a given discrete distribution since the probability mass function may take the same maximum value at several points x1, x2, etc. The most extreme case occurs in uniform distributions, where all values occur equally frequently.
A mode of a continuous probability distribution is often considered to be any value x at which its probability density function has a locally maximum value. When the probability density function of a continuous distribution has multiple local maxima it is common to refer to all of the local maxima as modes of the distribution, so any peak is a mode. Such a continuous distribution is called multimodal (as opposed to unimodal).
In symmetric unimodal distributions, such as the normal distribution, the mean (if defined), median and mode all coincide. For samples, if it is known that they are drawn from a symmetric unimodal distribution, the sample mean can be used as an estimate of the population mode.


== Mode of a sample ==
The mode of a sample is the element that occurs most often in the collection. For example, the mode of the sample [1, 3, 6, 6, 6, 6, 7, 7, 12, 12, 17] is 6. Given the list of data [1, 1, 2, 4, 4] its mode is not unique. A dataset, in such a case, is said to be bimodal, while a set with more than two modes may be described as multimodal.
For a sample from a continuous distribution, such as [0.935..., 1.211..., 2.430..., 3.668..., 3.874...], the concept is unusable in its raw form, since no two values will be exactly the same, so each value will occur precisely once. In order to estimate the mode of the underlying distribution, the usual practice is to  discretize the data by assigning frequency values to intervals of equal distance, as for making a histogram, effectively replacing the values by the midpoints of the
intervals they are assigned to. The mode is then the value where the histogram reaches its peak. For small or middle-sized samples the outcome of this procedure is sensitive to the choice of interval width if chosen too narrow or too wide; typically one should have a sizable fraction of the data concentrated in a relatively small number of intervals (5 to 10), while the fraction of the data falling outside these intervals is also sizable. An alternate approach is kernel density estimation, which essentially blurs point samples to produce a continuous estimate of the probability density function which can provide an estimate of the mode.
The following MATLAB (or Octave) code example computes the mode of a sample:

The algorithm requires as a first step to sort the sample in ascending order. It then computes the discrete derivative of the sorted list and finds the indices where this derivative is positive. Next it computes the discrete derivative of this set of indices, locating the maximum of this derivative of indices, and finally evaluates the sorted sample at the point where that maximum occurs, which corresponds to the last member of the stretch of repeated values.


== Comparison of mean, median and mode ==


=== Use ===
Unlike mean and median, the concept of mode also makes sense for "nominal data" (i.e., not consisting of numerical values in the case of mean, or even of ordered values in the case of median). For example, taking a sample of Korean family names, one might find that "Kim" occurs more often than any other name. Then "Kim" would be the mode of the sample. In any voting system where a plurality determines victory, a single modal value determines the victor, while a multi-modal outcome would require some tie-breaking procedure to take place.
Unlike median, the concept of mode makes sense for any random variable assuming values from a vector space, including the real numbers (a one-dimensional vector space) and the integers (which can be considered embedded in the reals). For example, a distribution of points in the plane will typically have a mean and a mode, but the concept of median does not apply. The median makes sense when there is a linear order on the possible values. Generalizations of the concept of median to higher-dimensional spaces are the geometric median and the centerpoint.


=== Uniqueness and definedness ===
For some probability distributions, the expected value may be infinite or undefined, but if defined, it is unique. The mean of a (finite) sample is always defined. The median is the value such that the fractions not exceeding it and not falling below it are each at least 1/2. It is not necessarily unique, but never infinite or totally undefined. For a data sample it is the "halfway" value when the list of values is ordered in increasing value, where usually for a list of even length the numerical average is taken of the two values closest to "halfway". Finally, as said before, the mode is not necessarily unique. Certain pathological distributions (for example, the Cantor distribution) have no defined mode at all. For a finite data sample, the mode is one (or more) of the values in the sample.


=== Properties ===
Assuming definedness, and for simplicity uniqueness, the following are some of the most interesting properties.

All three measures have the following property: If the random variable (or each value from the sample) is subjected to the linear or affine transformation, which replaces X by aX + b, so are the mean, median and mode.
Except for extremely small samples, the mode is insensitive to "outliers" (such as occasional, rare, false experimental readings). The median is also very robust in the presence of outliers, while the mean is rather sensitive.
In continuous unimodal distributions the median often lies between the mean and the mode, about one third of the way going from mean to mode. In a formula, median ≈ (2 × mean + mode)/3. This rule, due to Karl Pearson, often applies to slightly non-symmetric distributions that resemble a normal distribution, but it is not always true and in general the three statistics can appear in any order.
For unimodal distributions, the mode is within √3 standard deviations of the mean, and the root mean square deviation about the mode is between the standard deviation and twice the standard deviation.


=== Example for a skewed distribution ===
An example of a skewed distribution is personal wealth: Few people are very rich, but among those some are extremely rich. However, many are rather poor.

A well-known class of distributions that can be arbitrarily skewed is given by the log-normal distribution. It is obtained by transforming a random variable X having a normal distribution into random variable Y = eX. Then the logarithm of random variable Y is normally distributed, hence the name.
Taking the mean μ of X to be 0, the median of Y will be 1, independent of the standard deviation σ of X. This is so because X has a symmetric distribution, so its median is also 0. The transformation from X to Y is monotonic, and so we find the median e0 = 1 for Y.
When X has standard deviation σ = 0.25, the distribution of Y is weakly skewed.""",
    tier=2,
    domain="statistics",
    source="Wikipedia, 'Mode (statistics)'",
    source_url="https://en.wikipedia.org/wiki/Mode_%28statistics%29",
))

register_atom(Atom(
    atom_type="formula",
    name="variance",
    content="""In probability theory and statistics, variance is the expected value of the squared deviation from the mean of a random variable. The standard deviation is obtained as the square root of the variance. Variance is a measure of dispersion, meaning it is a measure of how far a set of numbers are spread out from their average value. It is the second central moment of a distribution, and the covariance of the random variable with itself, and it is often represented by ⁠
  
    
      
        
          σ
          
            2
          
        
      
    
    {\\displaystyle \\sigma ^{2}}
  
⁠, ⁠
  
    
      
        
          s
          
            2
          
        
      
    
    {\\displaystyle s^{2}}
  
⁠, ⁠
  
    
      
        Var
        ⁡
        (
        X
        )
      
    
    {\\displaystyle \\operatorname {Var} (X)}
  
⁠, ⁠
  
    
      
        V
        (
        X
        )
      
    
    {\\displaystyle V(X)}
  
⁠, or ⁠
  
    
      
        
          V
        
        (
        X
        )
      
    
    {\\displaystyle \\mathbb {V} (X)}
  
⁠.
An advantage of variance as a measure of dispersion is that it is more amenable to algebraic manipulation than other measures of dispersion such as the expected absolute deviation; for example, the variance of a sum of uncorrelated random variables is equal to the sum of their variances. A disadvantage of the variance for practical applications is that, unlike the standard deviation, its units differ from the random variable, which is why the standard deviation is more commonly reported as a measure of dispersion once the calculation is finished. Another disadvantage is that the variance is not finite for many distributions.
There are two distinct concepts that are both called "variance". One, as discussed above, is part of a theoretical probability distribution and is defined by an equation. The other variance is a characteristic of a set of observations. When variance is calculated from observations, those observations are typically measured from a real-world system. If all possible observations of the system are present, then the calculated variance is called the population variance. Normally, however, only a subset is available, and the variance calculated from this is called the sample variance. The variance calculated from a sample is considered an estimate of the full population variance. There are multiple ways to estimate the population variance on the basis of the sample variance, as discussed in the section below.
The two kinds of variance are closely related. To see how, consider that a theoretical probability distribution can be used as a generator of hypothetical observations. If an infinite number of observations are generated using a distribution, then the sample variance calculated from that infinite set will match the value calculated using the distribution's equation for variance. Variance has a central role in statistics, where some ideas that use it include descriptive statistics, statistical inference, hypothesis testing, goodness of fit, and Monte Carlo sampling.


== Definition ==
The variance of a random variable 
  
    
      
        X
      
    
    {\\displaystyle X}
  
 is the expected value of the squared deviation from the mean of ⁠
  
    
      
        X
      
    
    {\\displaystyle X}
  
⁠, ⁠
  
    
      
        μ
        =
        E
        ⁡
        [
        X
        ]
      
    
    {\\displaystyle \\mu =\\operatorname {E} [X]}
  
⁠:

  
    
      
        Var
        ⁡
        (
        X
        )
        =
        E
        ⁡
        
          [
          
            (
            X
            −
            μ
            
              )
              
                2
              
            
          
          ]
        
        .
      
    
    {\\displaystyle \\operatorname {Var} (X)=\\operatorname {E} \\left[(X-\\mu )^{2}\\right].}
  

This definition encompasses random variables that are generated by processes that are discrete, continuous, neither, or mixed. The variance can also be thought of as the covariance of a random variable with itself:

  
    
      
        Var
        ⁡
        (
        X
        )
        =
        Cov
        ⁡
        (
        X
        ,
        X
        )
        .
      
    
    {\\displaystyle \\operatorname {Var} (X)=\\operatorname {Cov} (X,X).}
  

The variance is also equivalent to the second cumulant of a probability distribution that generates ⁠
  
    
      
        X
      
    
    {\\displaystyle X}
  
⁠. The variance is typically designated as ⁠
  
    
      
        Var
        ⁡
        (
        X
        )
      
    
    {\\displaystyle \\operatorname {Var} (X)}
  
⁠, or sometimes as 
  
    
      
        V
        (
        X
        )
      
    
    {\\displaystyle V(X)}
  
 or ⁠
  
    
      
        
          V
        
        (
        X
        )
      
    
    {\\displaystyle \\mathbb {V} (X)}
  
⁠, or symbolically as ⁠
  
    
      
        
          σ
          
            X
          
          
            2
          
        
      
    
    {\\displaystyle \\sigma _{X}^{2}}
  
⁠ or simply 
  
    
      
        
          σ
          
            2
          
        
      
    
    {\\displaystyle \\sigma ^{2}}
  
 (pronounced "sigma squared").""",
    tier=3,
    domain="statistics",
    source="Wikipedia, 'Variance'",
    source_url="https://en.wikipedia.org/wiki/Variance",
))

register_atom(Atom(
    atom_type="formula",
    name="std_dev",
    content="""In statistics, the standard deviation is a measure of the amount of variation of the values of a variable about its (arithmetic) average. A low standard deviation indicates that the values of a set tend to be close to their average, while a high standard deviation indicates that the values are spread out over a wider range.  Standard deviation may be abbreviated SD or std dev, and is most commonly represented in mathematical texts and equations by the lowercase Greek letter σ (sigma).
The standard deviation of a random variable, sample, statistical population, data set or probability distribution is the square root of its variance (the variance being the average of the squared deviations from the mean). A useful property of the standard deviation is that, unlike the variance, it is expressed in the same unit as the data. Standard deviation can also be used to calculate standard error for a finite sample, and to determine statistical significance.
When only a sample of data from a population is available, the term standard deviation of the sample or sample standard deviation can refer to either the above-mentioned quantity as applied to those data, or to a modified quantity that is an unbiased estimate of the population standard deviation (the standard deviation of the entire population).


== Relationship with standard error and statistical significance ==
The standard deviation of a population or sample and the standard error of a statistic (e.g., of the sample mean) are quite different, but related. The sample mean's standard error is the standard deviation of the set of means that would be found by drawing an infinite number of repeated samples from the population and computing a mean for each sample.  The mean's standard error turns out to equal the population standard deviation divided by the square root of the sample size, and is estimated by using the sample standard deviation divided by the square root of the sample size. For example, a poll's standard error (what is reported as the margin of error of the poll) is the expected standard deviation of the estimated mean if the same poll were to be conducted multiple times. Thus, the standard error estimates the standard deviation of an estimate, which itself measures how much the estimate depends on the particular sample that was taken from the population.
In science, it is common to report both the standard deviation of the data (as a summary statistic) and the standard error of the estimate (as a measure of potential error in the findings). By convention, only effects more than two standard errors away from a null expectation are considered "statistically significant", a safeguard against spurious conclusion that is really due to random sampling error.


== Basic examples ==


=== Population standard deviation of grades of eight students ===
Suppose that the entire population of interest is eight students in a particular class.
Their marks are the following eight values:

  
    
      
        2
        ,
         
        4
        ,
         
        4
        ,
         
        4
        ,
         
        5
        ,
         
        5
        ,
         
        7
        ,
         
        9.
      
    
    {\\displaystyle 2,\\ 4,\\ 4,\\ 4,\\ 5,\\ 5,\\ 7,\\ 9.}
  

For a finite set of numbers, the population standard deviation is found by taking the square root of the average of the squared deviations of the values subtracted from their average value, that is:

  
    
      
        σ
        =
        
          
            
              a
              v
              e
              r
              a
              g
              e
            
            
              (
              
                (
                v
                −
                μ
                
                  )
                  
                    2
                  
                
                
                   for 
                
                v
                ∈
                
                  v
                  a
                  l
                  u
                  e
                  s
                
              
              )
            
          
        
        
           where 
        
        μ
        =
        
          a
          v
          e
          r
          a
          g
          e
        
        (
        
          v
          a
          l
          u
          e
          s
        
        )
        .
      
    
    {\\displaystyle \\sigma ={\\sqrt {\\mathrm {average} \\left((v-\\mu )^{2}{\\text{ for }}v\\in \\mathrm {values} \\right)}}{\\text{ where }}\\mu =\\mathrm {average} (\\mathrm {values} ).}
  

These eight data points have the mean (average) of 5:

  
    
      
        μ
        =
        
          
            
              2
              +
              4
              +
              4
              +
              4
              +
              5
              +
              5
              +
              7
              +
              9
            
            8
          
        
        =
        
          
            40
            8
          
        
        =
        5.
      
    
    {\\displaystyle \\mu ={\\frac {2+4+4+4+5+5+7+9}{8}}={\\frac {40}{8}}=5.}
  

First, calculate the deviations of each data point from the mean, and square the result of each:

  
    
      
        
          
            
              
                (
                2
                −
                5
                
                  )
                  
                    2
                  
                
                =
                (
                −
                3
                
                  )
                  
                    2
                  
                
                =
                9
              
              
              
                (
                5
                −
                5
                
                  )
                  
                    2
                  
                
                =
                
                  0
                  
                    2
                  
                
                =
                0
              
            
            
              
                (
                4
                −
                5
                
                  )
                  
                    2
                  
                
                =
                (
                −
                1
                
                  )
                  
                    2
                  
                
                =
                1
              
              
              
                (
                5
                −
                5
                
                  )
                  
                    2
                  
                
                =
                
                  0
                  
                    2
                  
                
                =
                0
              
            
            
              
                (
                4
                −
                5
                
                  )
                  
                    2
                  
                
                =
                (
                −
                1
                
                  )
                  
                    2
                  
                
                =
                1
              
              
              
                (
                7
                −
                5
                
                  )
                  
                    2
                  
                
                =
                
                  2
                  
                    2
                  
                
                =
                4
              
""",
    tier=3,
    domain="statistics",
    source="Wikipedia, 'Standard deviation'",
    source_url="https://en.wikipedia.org/wiki/Standard_deviation",
))

register_atom(Atom(
    atom_type="formula",
    name="z_score",
    content="""In statistics, the standard score or z-score is the number of standard deviations by which the value of a raw score (i.e., an observed value or data point) is above or below the mean value of what is being observed or measured. Raw scores above the mean have positive standard scores, while those below the mean have negative standard scores. 
It is calculated by subtracting the population mean from an individual raw score and then dividing the difference by the population standard deviation. This process of converting a raw score into a standard score is called standardizing or normalizing (however, "normalizing" can refer to many types of ratios; see Normalization for more). 
Standard scores are most commonly called z-scores; the two terms may be used interchangeably, as they are in this article. Other equivalent terms in use include z-value, z-statistic, normal score, standardized variable and pull in high energy physics. 
Computing a z-score requires knowledge of the mean and standard deviation of the complete population to which a data point belongs; if one only has a sample of observations from the population, then the analogous computation using the sample mean and sample standard deviation yields the t-statistic.


== Calculation ==
If the population mean and population standard deviation are known, a raw score 
x is converted into a standard score by

  
    
      
        z
        =
        
          
            
              x
              −
              μ
            
            σ
          
        
      
    
    {\\displaystyle z={\\frac {x-\\mu }{\\sigma }}}
  

where:

μ is the mean of the population,
σ is the standard deviation of the population.
The absolute value of z represents the distance between that raw score x and the population mean in units of the standard deviation. z is negative when the raw score is below the mean, positive when above.
Calculating z using this formula requires use of the population mean and the population standard deviation, not the sample mean or sample deviation. However, knowing the true mean and standard deviation of a population is often an unrealistic expectation, except in cases such as standardized testing, where the entire population is measured.
When the population mean and the population standard deviation are unknown, the standard score may be estimated by using the sample mean and sample standard deviation as estimates of the population values.
In these cases, the z-score is given by

  
    
      
        z
        =
        
          
            
              x
              −
              
                
                  
                    x
                    ¯
                  
                
              
            
            S
          
        
      
    
    {\\displaystyle z={\\frac {x-{\\bar {x}}}{S}}}
  

where:

  
    
      
        
          
            
              x
              ¯
            
          
        
      
    
    {\\displaystyle {\\bar {x}}}
  
 is the mean of the sample,
S is the standard deviation of the sample.
Though it should always be stated, the distinction between use of the population and sample statistics often is not made. In either case, the numerator and denominator of the equations have the same units of measure so that the units cancel out through division and z is left as a dimensionless quantity.


== Applications ==


=== Z-test ===

The z-score is often used in the z-test in standardized testing – the analog of the Student's t-test for a population whose parameters are known, rather than estimated. As it is very unusual to know the entire population, the t-test is much more widely used.


=== Prediction intervals ===

The standard score can be used in the calculation of prediction intervals. A prediction interval [L,U], consisting of a lower endpoint designated L and an upper endpoint designated U, is an interval such that a future observation X will lie in the interval with high probability 
  
    
      
        γ
      
    
    {\\displaystyle \\gamma }
  
, i.e.

  
    
      
        Pr
        (
        L
        <
        X
        <
        U
        )
        =
        γ
        ,
      
    
    {\\displaystyle \\Pr(L<X<U)=\\gamma ,}
  

For the standard score Z of X it gives:

  
    
      
        Pr
        
          
            (
            
              
                
                  
                    L
                    −
                    μ
                  
                  σ
                
              
              <
              Z
              <
              
                
                  
                    U
                    −
                    μ
                  
                  σ
                
              
            
            )
          
        
        =
        γ
        .
      
    
    {\\displaystyle \\Pr {\\left({\\frac {L-\\mu }{\\sigma }}<Z<{\\frac {U-\\mu }{\\sigma }}\\right)}=\\gamma .}
  

By determining the quantile z such that

  
    
      
        Pr
        
          (
          
            −
            z
            <
            Z
            <
            z
          
          )
        
        =
        γ
      
    
    {\\displaystyle \\Pr \\left(-z<Z<z\\right)=\\gamma }
  

it follows:

  
    
      
        L
        =
        μ
        −
        z
        σ
        ,
         
        U
        =
        μ
        +
        z
        σ
      
    
    {\\displaystyle L=\\mu -z\\sigma ,\\ U=\\mu +z\\sigma }
  


=== Process control ===
In process control applications, the Z value provides an assessment of the degree to which a process is operating off-target.


=== Comparison of scores measured on different scales: ACT and SAT ===

When scores are measured on different scales, they may be converted to z-scores to aid comparison. Dietz et al. give the following example, comparing student scores on the (old) SAT and ACT high school tests. The table shows the mean and standard deviation for total scores on the SAT and ACT. Suppose that student A scored 1800 on the SAT, and student B scored 24 on the ACT.""",
    tier=3,
    domain="statistics",
    source="Wikipedia, 'Standard score'",
    source_url="https://en.wikipedia.org/wiki/Standard_score",
))

register_atom(Atom(
    atom_type="formula",
    name="linear_regression",
    content="""In statistics, simple linear regression (SLR) is a linear regression model with a single explanatory variable. That is, it concerns two-dimensional sample points with one independent variable and one dependent variable (conventionally, the x and y coordinates in a Cartesian coordinate system) and finds a linear function (a non-vertical straight line) that, as accurately as possible, predicts the dependent variable values as a function of the independent variable.
The adjective simple refers to the fact that the outcome variable is related to a single predictor.
It is common to make the additional stipulation that the ordinary least squares (OLS) method should be used: the accuracy of each predicted value is measured by its squared residual (vertical distance between the point of the data set and the fitted line), and the goal is to make the sum of these squared deviations as small as possible. 
In this case, the slope of the fitted line is equal to the correlation between y and x corrected by the ratio of standard deviations of these variables. The intercept of the fitted line is such that the line passes through the center of mass (x, y) of the data points.


== Formulation and computation ==
Consider the model function

  
    
      
        y
        =
        α
        +
        β
        x
        ,
      
    
    {\\displaystyle y=\\alpha +\\beta x,}
  

which describes a line with slope β and y-intercept α. In general, such a relationship may not hold exactly for the largely unobserved population of values of the independent and dependent variables; we call the unobserved deviations from the above equation the errors.   Suppose we observe n data pairs and call them {(xi, yi), i = 1, ..., n}. We can describe the underlying relationship between yi and xi involving this error term εi by

  
    
      
        
          y
          
            i
          
        
        =
        α
        +
        β
        
          x
          
            i
          
        
        +
        
          ε
          
            i
          
        
        .
      
    
    {\\displaystyle y_{i}=\\alpha +\\beta x_{i}+\\varepsilon _{i}.}
  

This relationship between the true (but unobserved) underlying parameters α and β and the data points is called a linear regression model.
The goal is to find estimated values 
  
    
      
        
          
            
              α
              ^
            
          
        
      
    
    {\\displaystyle {\\widehat {\\alpha }}}
  
 and 
  
    
      
        
          
            
              β
              ^
            
          
        
      
    
    {\\displaystyle {\\widehat {\\beta }}}
  
 for the parameters α and β which would provide the "best" fit in some sense for the data points. As mentioned in the introduction, in this article the "best" fit will be understood as in the least-squares approach: a line that minimizes the sum of squared residuals (see also Errors and residuals) 
  
    
      
        
          
            
              
                ε
                ^
              
            
          
          
            i
          
        
      
    
    {\\displaystyle {\\widehat {\\varepsilon }}_{i}}
  
 (differences between actual and predicted values of the dependent variable y), each of which is given by, for any candidate parameter values 
  
    
      
        α
      
    
    {\\displaystyle \\alpha }
  
 and 
  
    
      
        β
      
    
    {\\displaystyle \\beta }
  
,

  
    
      
        
          
            
              
                ε
                ^
              
            
          
          
            i
          
        
        =
        
          y
          
            i
          
        
        −
        α
        −
        β
        
          x
          
            i
          
        
        .
      
    
    {\\displaystyle {\\widehat {\\varepsilon }}_{i}=y_{i}-\\alpha -\\beta x_{i}.}
  

In other words, 
  
    
      
        
          
            
              α
              ^
            
          
        
      
    
    {\\displaystyle {\\widehat {\\alpha }}}
  
 and 
  
    
      
        
          
            
              β
              ^
            
          
        
      
    
    {\\displaystyle {\\widehat {\\beta }}}
  
 solve the following minimization problem:

  
    
      
        (
        
          
            
              α
              ^
            
          
        
        ,
        
        
          
            
              β
              ^
            
          
        
        )
        =
        argmin
        ⁡
        
          (
          
            Q
            (
            α
            ,
            β
            )
          
          )
        
        ,
      
    
    {\\displaystyle ({\\hat {\\alpha }},\\,{\\hat {\\beta }})=\\operatorname {argmin} \\left(Q(\\alpha ,\\beta )\\right),}
  

where the objective function Q is:

  
    
      
        Q
        (
        α
        ,
        β
        )
        =
        
          ∑
          
            i
            =
            1
          
          
            n
          
        
        
          
            
              
                ε
                ^
              
            
          
          
            i
          
          
            
            2
          
        
        =
        
          ∑
          
            i
            =
            1
          
          
            n
          
        
        (
        
          y
          
            i
          
        
        −
        α
        −
        β
        
          x
          
            i
          
        
        
          )
          
            2
          
        
         
        .
      
    
    {\\displaystyle Q(\\alpha ,\\beta )=\\sum _{i=1}^{n}{\\widehat {\\varepsilon }}_{i}^{\\,2}=\\sum _{i=1}^{n}(y_{i}-\\alpha -\\beta x_{i})^{2}\\ .}
  

By expanding to get a quadratic expression in 
  
    
      
        α
      
    
    {\\displaystyle \\alpha }
  
 and 
  
    
      
        β
        ,
      
    
    {\\displaystyle \\beta ,}
  
 we can derive minimizing values of the function arguments, denoted 
  
    
      
        
          
            
              α
              ^
            
          
        
      
    
    {\\displaystyle {\\widehat {\\alpha }}}
  
 and 
  
    
      
        
          
            
              β
              ^
            
          
        
      
    
    {\\displaystyle {\\widehat {\\beta }}}
  
:

  
    
      
        
          
            
              
                
                  
                    
                      α
                      ^
                    
                  
                
              
              
                
                =
                
                  
                    
                      y
                      ¯
                    
                  
                
                −
                
                  
                    
                      β
                      ^
                    
                  
                
                
                
                  
                    
                      x
                      ¯
                    
                  
                
                ,
              
            
            
              
                
                  
                    
                      β
                      ^
                    
                  
                
              
              
                
                =
                
                  
                    
                      
                        ∑
                        
                          i
                          =
                          1
                        
                        
     """,
    tier=4,
    domain="statistics",
    source="Wikipedia, 'Simple linear regression'",
    source_url="https://en.wikipedia.org/wiki/Simple_linear_regression",
))

register_atom(Atom(
    atom_type="formula",
    name="correlation",
    content="""In statistics, the Pearson correlation coefficient (PCC), also known as Pearson's r, the Pearson product-moment correlation coefficient (PPMCC), or simply the unqualified correlation coefficient, is a correlation coefficient that measures linear correlation between two sets of data. It is the ratio between the covariance of two variables and the product of their standard deviations; thus, it is essentially a normalized measurement of the covariance, such that the result always has a value between −1 and 1. A key difference is that unlike covariance, this correlation coefficient does not have units, allowing comparison of the strength of the joint association between different pairs of random variables that do not necessarily have the same units. As with covariance itself, the measure can only reflect a linear correlation of variables, and ignores many other types of relationships or correlations. As a simple example, one would expect the age and height of a sample of children from a school to have a Pearson correlation coefficient significantly greater than 0, but less than 1 (as 1 would represent an unrealistically perfect correlation).


== Naming and history ==
It was developed by Karl Pearson from a related idea introduced by Francis Galton in the 1880s, and for which the mathematical formula was derived and published by Auguste Bravais in 1844. The naming of the coefficient is thus an example of Stigler's Law.


== Intuitive explanation ==
The correlation coefficient can be derived by shifting the x and y data values so they each have zero average over the population of n individuals, collecting each data set to form the coordinates of an n-dimensional vector, and computing the cosine between these two vector directions. This expression is therefore a number between -1 and 1 and is equal to unity whenever the two vectors are colinear, i.e. when the individual x and y values obey a consistent linear relationship.
The formulas below may be derived from the dot product and length formulas for vectors.


== Definition ==
Pearson's correlation coefficient is the covariance of the two variables divided by the product of their standard deviations. The formal definition involves a "product moment", that is, the mean (the first moment about the origin) of the product of the mean-adjusted random variables.


=== For a population ===
Pearson's correlation coefficient, when applied to a population, is commonly represented by the Greek letter ρ (rho) and may be referred to as the population correlation coefficient or the population Pearson correlation coefficient. Given a pair of random variables 
  
    
      
        (
        X
        ,
        Y
        )
      
    
    {\\displaystyle (X,Y)}
  
 (for example, Height and Weight), the formula for ρ is

  
    
      
        
          ρ
          
            X
            ,
            Y
          
        
        =
        
          
            
              cov
              ⁡
              (
              X
              ,
              Y
              )
            
            
              
                σ
                
                  X
                
              
              
                σ
                
                  Y
                
              
            
          
        
      
    
    {\\displaystyle \\rho _{X,Y}={\\frac {\\operatorname {cov} (X,Y)}{\\sigma _{X}\\sigma _{Y}}}}
  

where

  
    
      
        cov
      
    
    {\\displaystyle \\operatorname {cov} }
  
 is the covariance

  
    
      
        
          σ
          
            X
          
        
      
    
    {\\displaystyle \\sigma _{X}}
  
 is the standard deviation of  
  
    
      
        X
      
    
    {\\displaystyle X}
  

  
    
      
        
          σ
          
            Y
          
        
      
    
    {\\displaystyle \\sigma _{Y}}
  
 is the standard deviation of  
  
    
      
        Y
      
    
    {\\displaystyle Y}
  
.
The formula for 
  
    
      
        cov
        ⁡
        (
        X
        ,
        Y
        )
      
    
    {\\displaystyle \\operatorname {cov} (X,Y)}
  
 can be expressed in terms of mean and expectation. Since

  
    
      
        cov
        ⁡
        (
        X
        ,
        Y
        )
        =
        
          
            E
          
        
        ⁡
        [
        (
        X
        −
        
          μ
          
            X
          
        
        )
        (
        Y
        −
        
          μ
          
            Y
          
        
        )
        ]
        ,
      
    
    {\\displaystyle \\operatorname {cov} (X,Y)=\\operatorname {\\mathbb {E} } [(X-\\mu _{X})(Y-\\mu _{Y})],}
  

the formula for 
  
    
      
        ρ
      
    
    {\\displaystyle \\rho }
  
 can also be written as

  
    
      
        
          ρ
          
            X
            ,
            Y
          
        
        =
        
          
            
              
                
                  E
                
              
              ⁡
              [
              (
              X
              −
              
                μ
                
                  X
                
              
              )
              (
              Y
              −
              
                μ
                
                  Y
                
              
              )
              ]
            
            
              
                σ
                
                  X
                
              
              
                σ
                
                  Y
                
              
            
          
        
      
    
    {\\displaystyle \\rho _{X,Y}={\\frac {\\operatorname {\\mathbb {E} } [(X-\\mu _{X})(Y-\\mu _{Y})]}{\\sigma _{X}\\sigma _{Y}}}}
  

where

  
    
      
        
          σ
          
            Y
          
        
      
    
    {\\displaystyle \\sigma _{Y}}
  
 and 
  
    
      
        
          σ
          
            X
          
        
      
    
    {\\displaystyle \\sigma _{X}}
  
 are defined as above

  
    
      
        
          μ
          
            X
          
        
      
    
    {\\displaystyle \\mu _{X}}
  
 is the mean of 
  
    
      
        X
      
    
    {\\displaystyle X}
  

  
    
      
        
          μ
          
            Y
          
        
      
    
    {\\displaystyle \\mu _{Y}}
  
 is the mean of 
  
    
      
        Y
      
    
    {\\displaystyle Y}
  

  
    
      
        
          
            E
          
        
      
    
    {\\displaystyle \\operatorname {\\mathbb {E} } }
  
 is the expectation.
The formula for 
  
    
      
        ρ
      
    
    {\\displaystyle \\rho }
  
 can be expressed in terms of uncentered moments.""",
    tier=4,
    domain="statistics",
    source="Wikipedia, 'Pearson correlation coefficient'",
    source_url="https://en.wikipedia.org/wiki/Pearson_correlation_coefficient",
))

register_atom(Atom(
    atom_type="formula",
    name="hypothesis_test",
    content="""A statistical hypothesis test is a method of statistical inference used to decide whether the data provide sufficient evidence to reject a particular hypothesis. A statistical hypothesis test typically involves a calculation of a test statistic. Then a decision is made, either by comparing the test statistic to a critical value or equivalently by evaluating a p-value computed from the test statistic. Roughly 100 specialized statistical tests are in use.


== Definition of terms ==

The goal of a hypothesis test is to establish whether certain properties of a statistical population are true by examining sample data. Typically, the population is modelled by a random variable whose distribution has unknown parameters. For example, a medical trial may wish to establish whether a particular drug is effective in treating high blood pressure, with "the change in blood pressure observed in a patient who takes the drug" being the random variable. An example hypothesis could be "the mean change in blood pressure is zero" or "the mean change in blood pressure is negative". In general, any statement about the parameters describing a population can be a hypothesis (but not a statement about the sample).
The test compares two hypotheses: a default "null" hypothesis (denoted H0) and its negation, the "alternative" hypothesis (H1). Typically the test will select a null hypothesis that the intervention being studied has no effect, or that the population parameter takes some "obvious" value. A test statistic is computed from the given sample data, and the tester calculates the conditional probability of observing a value at least this extreme, supposing the null hypothesis is true. If this probability (called the p-value) is less than the significance level of the test (denoted 
  
    
      
        α
      
    
    {\\displaystyle \\alpha }
  
), then the null hypothesis is rejected. The test does not conclude that the null hypothesis is false, or that the probability that the null hypothesis is false is less than 
  
    
      
        α
      
    
    {\\displaystyle \\alpha }
  
.
Because it is usually impossible to definitely establish whether the hypothesis being tested is true or false from a sample, the conclusion of a hypothesis test is not certain to be correct. There are two possible classes of error:

A type I error, in which the null hypothesis is rejected despite the null hypothesis being true, with probability 
  
    
      
        α
        =
        P
        (
        
          reject 
        
        
          H
          
            0
          
        
        
          |
        
        
          H
          
            0
          
        
        )
      
    
    {\\displaystyle \\alpha =P({\\text{reject }}H_{0}|H_{0})}
  
. This is the same as the significance level of the test.
A type II error, in which the null hypothesis is accepted despite the alternative hypothesis being true, with probability 
  
    
      
        β
        =
        P
        (
        
          accept 
        
        
          H
          
            0
          
        
        
          |
        
        
          H
          
            1
          
        
        )
      
    
    {\\displaystyle \\beta =P({\\text{accept }}H_{0}|H_{1})}
  
. The quantity 
  
    
      
        1
        −
        β
      
    
    {\\displaystyle 1-\\beta }
  
 is called the power of the test.
Some further definitions:

Simple hypothesis: Any hypothesis which specifies the population distribution completely.
Composite hypothesis: Any hypothesis which does not specify the population distribution completely.
Positive data: Data that enable the investigator to reject a null hypothesis.

Critical values of a statistical test are the boundaries of the acceptance region of the test. The acceptance region is the set of values of the test statistic for which the null hypothesis is not rejected. Depending on the shape of the acceptance region, there can be one or more than one critical value.
Region of rejection / Critical region: The set of values of the test statistic for which the null hypothesis is rejected.
Size: For simple hypotheses, this is the test's probability of incorrectly rejecting the null hypothesis. The false positive rate. For composite hypotheses this is the supremum of the probability of rejecting the null hypothesis over all cases covered by the null hypothesis. The complement of the false positive rate is termed specificity in biostatistics. ("This is a specific test. Because the result is positive, we can confidently say that the patient has the condition.") See sensitivity and specificity and type I and type II errors for exhaustive definitions.
Statistical significance test: A predecessor to the statistical hypothesis test (see the Origins section). An experimental result was said to be statistically significant if a sample was sufficiently inconsistent with the (null) hypothesis. This was variously considered common sense, a pragmatic heuristic for identifying meaningful experimental results, a convention establishing a threshold of statistical evidence or a method for drawing conclusions from data. The statistical hypothesis test added mathematical rigor and philosophical consistency to the concept by making the alternative hypothesis explicit. The term is loosely used for the modern version which is now part of statistical hypothesis testing.
Conservative test: A test is conservative if, when constructed for a given nominal significance level, the true probability of incorrectly rejecting the null hypothesis is never greater than the nominal level.
Exact test
A statistical hypothesis test compares a test statistic (z or t for examples) to a threshold. The test statistic (the formula found in the table below) is based on optimality. For a fixed level of Type I error rate, use of these statistics minimizes Type II error rates (equivalent to maximizing power). The following terms describe tests in terms of such optimality:

Most powerful test: For a given size or significance level, the test with the greatest power (probability of rejection) for a given value of the parameter(s) being tested, contained in the alternative hypothesis.
Uniformly most powerful test (UMP)


== History ==

While hypothesis testing was popularized early in the 20th century, early forms were used in the 1700s. The first use is credited to John Arbuthnot (1710), followed by Pierre-Simon Laplace (1770s), in analyzing the human sex ratio at birth; see § Human sex ratio.
1778: Pierre Laplace compares the birthrates of boys and girls in multiple European cities. He states: "it is natural to conclude that these possibilities are very nearly in the same ratio". Thus, the null hypothesis in this case that the birthrates of boys and girls should be equal given "conventional wisdom".
1900: Karl Pearson develops the chi squared test to determine "whether a given form of frequency curve will effectively describe the samples drawn from a given population." Thus the null hypothesis is that a population is described by some distribution predicted by theory. He uses as an example the numbers of five and sixes in the Weldon dice throw data.
1904: Karl Pearson develops the concept of "contingency" in order to determine whether outcomes are independent of a given categorical factor. Here the null hypothesis is by default that two things are unrelated (e.g. scar formation and death rates from smallpox).""",
    tier=5,
    domain="statistics",
    source="Wikipedia, 'Statistical hypothesis test'",
    source_url="https://en.wikipedia.org/wiki/Statistical_hypothesis_test",
))

register_atom(Atom(
    atom_type="formula",
    name="confidence_interval",
    content="""According to frequentist inference, a confidence interval (CI) is a range of values which is likely to contain (in repeated sampling) the true value of an unknown statistical parameter, such as a population mean. Rather than reporting a single point estimate (e.g. "the average screen time is 3 hours per day"), a confidence interval provides a range, such as 2 to 4 hours, along with a specified confidence level, typically 95%. 
A 95% confidence level does not imply a 95% probability that the true parameter lies within a particular calculated interval, which is instead associated with the credible interval in Bayesian inference. The confidence level instead reflects the long-run reliability of the method used to generate the interval. In other words, if the same sampling procedure were repeated 100 times from the same population, approximately 95 of the resulting intervals would be expected to contain the true population mean. The frequentist approach sees the true population mean as a fixed unknown constant, while the confidence interval is calculated using data from a random sample. Because the sample is random, the interval endpoints are random variables. 


== Definition ==
Let 
  
    
      
        X
      
    
    {\\displaystyle X}
  
 be a random sample from a probability distribution with statistical parameter 
  
    
      
        (
        θ
        ,
        φ
        )
      
    
    {\\displaystyle (\\theta ,\\varphi )}
  
. Here, 
  
    
      
        θ
      
    
    {\\displaystyle \\theta }
  
 is the quantity to be estimated, while 
  
    
      
        φ
      
    
    {\\displaystyle \\varphi }
  
 includes other parameters (if any) that determine the distribution. A confidence interval for the parameter 
  
    
      
        θ
      
    
    {\\displaystyle \\theta }
  
, with confidence level or coefficient 
  
    
      
        γ
      
    
    {\\displaystyle \\gamma }
  
, is an interval 
  
    
      
        (
        u
        (
        X
        )
        ,
        v
        (
        X
        )
        )
      
    
    {\\displaystyle (u(X),v(X))}
  
 determined by random variables 
  
    
      
        u
        (
        X
        )
      
    
    {\\displaystyle u(X)}
  
 and 
  
    
      
        v
        (
        X
        )
      
    
    {\\displaystyle v(X)}
  
 with the property:

  
    
      
        P
        (
        u
        (
        X
        )
        <
        θ
        <
        v
        (
        X
        )
        )
        =
        γ
        
        
          for all 
        
        (
        θ
        ,
        φ
        )
        .
      
    
    {\\displaystyle P(u(X)<\\theta <v(X))=\\gamma \\quad {\\text{for all }}(\\theta ,\\varphi ).}
  

The number 
  
    
      
        γ
      
    
    {\\displaystyle \\gamma }
  
, which is typically large (e.g. 0.95), is sometimes given in the form 
  
    
      
        1
        −
        α
      
    
    {\\displaystyle 1-\\alpha }
  
 (or as a percentage 
  
    
      
        100
        %
        ⋅
        (
        1
        −
        α
        )
      
    
    {\\displaystyle 100\\%\\cdot (1-\\alpha )}
  
), where 
  
    
      
        α
      
    
    {\\displaystyle \\alpha }
  
 is a small positive number, often 0.05. It means that the interval 
  
    
      
        (
        u
        (
        X
        )
        ,
        v
        (
        X
        )
        )
      
    
    {\\textstyle (u(X),v(X))}
  
 has a probability 
  
    
      
        γ
      
    
    {\\textstyle \\gamma }
  
 of covering the value of 
  
    
      
        θ
      
    
    {\\textstyle \\theta }
  
 in repeated sampling. 
In many applications, confidence intervals that have exactly the required confidence level are hard to construct, but approximate intervals can be computed. The rule for constructing the interval may be accepted if

  
    
      
        P
        (
        u
        (
        X
        )
        <
        θ
        <
        v
        (
        X
        )
        )
        ≈
         
        γ
      
    
    {\\displaystyle P(u(X)<\\theta <v(X))\\approx \\ \\gamma }
  

to an acceptable level of approximation. Alternatively, some authors simply require that

  
    
      
        P
        (
        u
        (
        X
        )
        <
        θ
        <
        v
        (
        X
        )
        )
        ≥
         
        γ
      
    
    {\\displaystyle P(u(X)<\\theta <v(X))\\geq \\ \\gamma }
  

When it is known that the coverage probability can be strictly larger than 
  
    
      
        γ
      
    
    {\\displaystyle \\gamma }
  
 for some parameter values, the confidence interval is called conservative, i.e., it errs on the safe side; which also means that the interval can be wider than need be.


=== Methods of derivation ===
There are many ways of calculating confidence intervals, and the best method depends on the situation. Two widely applicable methods are bootstrapping and the central limit theorem.""",
    tier=5,
    domain="statistics",
    source="Wikipedia, 'Confidence interval'",
    source_url="https://en.wikipedia.org/wiki/Confidence_interval",
))

register_atom(Atom(
    atom_type="formula",
    name="basic_prob",
    content="""Probability concerns events and numerical descriptions of how likely they are to occur.  The probability of an event is a number between 0 and 1; the larger the probability, the more likely an event is to occur. This number is often expressed as a percentage (%), ranging from 0% to 100%. A simple example is the tossing of a fair (unbiased) coin. Since the coin is fair, the two outcomes ("heads" and "tails") are both equally probable; the probability of "heads" equals the probability of "tails"; and since no other outcomes are possible, the probability of either "heads" or "tails" is 1/2 (which could also be written as 0.5 or 50%).
These concepts have been given an axiomatic mathematical formalization in probability theory, which is used widely in areas of study such as statistics, mathematics, science, finance, gambling, artificial intelligence, machine learning, computer science, game theory, and philosophy to, for example, draw inferences about the expected frequency of events. Probability theory is also used to describe the underlying mechanics and regularities of complex systems.


== Etymology ==

The word probability derives from the Latin probabilitas, which can also mean "probity", a measure of the authority of a witness in a legal case in Europe, and often correlated with the witness's nobility. In a sense, this differs much from the modern meaning of probability, which in contrast is a measure of the weight of empirical evidence, and is arrived at from inductive reasoning and statistical inference.


== Interpretations ==

When dealing with random experiments – i.e., experiments that are random and well-defined – in a purely theoretical setting (like tossing a coin), probabilities can be numerically described by the number of desired outcomes, divided by the total number of all outcomes.  This is referred to as theoretical probability (in contrast to empirical probability, dealing with probabilities in the context of real experiments). The probability is a number between 0 and 1; the larger the probability, the more likely the desired outcome is to occur. For example, tossing a coin twice will yield "head-head", "head-tail", "tail-head", and "tail-tail" outcomes. The probability of getting an outcome of "head-head" is 1 out of 4 outcomes, or, in numerical terms, 1/4, 0.25 or 25%. The probability of getting an outcome of at least one head is 3 out of 4, or 0.75, and this event is more likely to occur. However, when it comes to practical application, there are two major competing categories of probability interpretations, whose adherents hold different views about the fundamental nature of probability:

Objectivists assign numbers to describe some objective or physical state of affairs. The most popular version of objective probability is frequentist probability, which claims that the probability of a random event denotes the relative frequency of occurrence of an experiment's outcome when the experiment is repeated indefinitely. This interpretation considers probability to be the relative frequency "in the long run" of outcomes. A modification of this is propensity probability, which interprets probability as the tendency of some experiment to yield a certain outcome, even if it is performed only once.
Subjectivists assign numbers per subjective probability, that is, as a degree of belief. The degree of belief has been interpreted as "the price at which you would buy or sell a bet that pays 1 unit of utility if E, 0 if not E", although that interpretation is not universally agreed upon. The most popular version of subjective probability is Bayesian probability, which includes expert knowledge as well as experimental data to produce probabilities. The expert knowledge is represented by some (subjective) prior probability distribution. These data are incorporated in a likelihood function. The product of the prior and the likelihood, when normalized, results in a posterior probability distribution that incorporates all the information known to date. By Aumann's agreement theorem, Bayesian agents whose prior beliefs are similar will end up with similar posterior beliefs. However, sufficiently different priors can lead to different conclusions, regardless of how much information the agents share.


== History ==

The scientific study of probability is a modern development of mathematics. Gambling shows that there has been an interest in quantifying the ideas of probability throughout history, but exact mathematical descriptions arose much later. There are reasons for the slow development of the mathematics of probability. Whereas games of chance provided the impetus for the mathematical study of probability, fundamental issues  are still obscured by superstitions.
According to Richard Jeffrey, "Before the middle of the seventeenth century, the term 'probable' (Latin probabilis) meant approvable, and was applied in that sense, univocally, to opinion and to action. A probable action or opinion was one such as sensible people would undertake or hold, in the circumstances." However, in legal contexts especially, 'probable' could also apply to propositions for which there was good evidence.

The sixteenth-century Italian polymath Gerolamo Cardano demonstrated the efficacy of defining odds as the ratio of favourable to unfavourable outcomes (which implies that the probability of an event is given by the ratio of favourable outcomes to the total number of possible outcomes).
Aside from the elementary work by Cardano, the doctrine of probabilities dates to the correspondence of Pierre de Fermat and Blaise Pascal (1654). Christiaan Huygens (1657) gave the earliest known scientific treatment of the subject. Jakob Bernoulli's Ars Conjectandi (posthumous, 1713) and Abraham de Moivre's Doctrine of Chances (1718) treated the subject as a branch of mathematics. See Ian Hacking's The Emergence of Probability and James Franklin's The Science of Conjecture for histories of the early development of the very concept of mathematical probability.
The theory of errors may be traced back to Roger Cotes's Opera Miscellanea (posthumous, 1722), but a memoir prepared by Thomas Simpson in 1755 (printed 1756) first applied the theory to the discussion of errors of observation. The reprint (1757) of this memoir lays down the axioms that positive and negative errors are equally probable, and that certain assignable limits define the range of all errors. Simpson also discusses continuous errors and describes a probability curve.
The first two laws of error that were proposed both originated with Pierre-Simon Laplace. The first law was published in 1774, and stated that the frequency of an error could be expressed as an exponential function of the numerical magnitude of the error – disregarding sign. The second law of error was proposed in 1778 by Laplace, and stated that the frequency of the error is an exponential function of the square of the error. The second law of error is called the normal distribution or the Gauss law. "It is difficult historically to attribute that law to Gauss, who in spite of his well-known precocity had probably not made this discovery before he was two years old."
Daniel Bernoulli (1778) introduced the principle of the maximum product of the probabilities of a system of concurrent errors.

Adrien-Marie Legendre (1805) developed the method of least squares, and introduced it in his Nouvelles méthodes pour la détermination des orbites des comètes (New Methods for Determining the Orbits of Comets).""",
    tier=2,
    domain="probability",
    source="Wikipedia, 'Probability'",
    source_url="https://en.wikipedia.org/wiki/Probability",
))

register_atom(Atom(
    atom_type="formula",
    name="conditional_prob",
    content="""In probability theory, conditional probability is a measure of the probability of an event occurring, given that another event (by assumption, presumption, assertion, or evidence) is already known to have occurred. This particular method relies on event A occurring with some sort of relationship with another event B. In this situation, the event A can be analyzed by a conditional probability with respect to B. If the event of interest is A and the event B is known or assumed to have occurred, "the conditional probability of A given B", or "the probability of A under the condition B", is usually written as P(A|B) or occasionally PB(A). This can also be understood as the fraction of probability B that intersects with A, or the ratio of the probabilities of both events happening to the "given" one happening (how many times A occurs rather than not assuming B has occurred): 

  
    
      
        P
        (
        A
        ∣
        B
        )
        =
        
          
            
              P
              (
              A
              ∩
              B
              )
            
            
              P
              (
              B
              )
            
          
        
      
    
    {\\displaystyle P(A\\mid B)={\\frac {P(A\\cap B)}{P(B)}}}
  
.
For example, the probability that any given person has a cough on any given day may be only 5%. But if we know or assume that the person is sick, then they are much more likely to be coughing. For example, the conditional probability that someone sick is coughing might be 75%, in which case we would have that P(Cough) = 5% and P(Cough|Sick) = 75 %. Although there is a relationship between A and B in this example, such a relationship or dependence between A and B is not necessary, nor do they have to occur simultaneously.
P(A|B) may or may not be equal to P(A), i.e., the unconditional probability or absolute probability of A. If P(A|B) = P(A), then events A and B are said to be independent: in such a case, knowledge about either event does not alter the likelihood of the other. P(A|B) (the conditional probability of A given B) typically differs from P(B|A). For example, if a person has dengue fever, the person might have a 90% chance of being tested as positive for the disease. In this case, what is being measured is that if event B (having dengue) has occurred, the probability of A (tested as positive) given that B occurred is 90%, simply writing P(A|B) = 90%. Alternatively, if a person is tested as positive for dengue fever, they may have only a 15% chance of actually having this rare disease due to high false positive rates. In this case, the probability of the event B (having dengue) given that the event A (testing positive) has occurred is 15% or P(B|A) = 15%. It should be apparent now that falsely equating the two probabilities can lead to various errors of reasoning, which is commonly seen through base rate fallacies.
While conditional probabilities can provide extremely useful information, limited information is often supplied or at hand. Therefore, it can be useful to reverse or convert a conditional probability using Bayes' theorem: 
  
    
      
        P
        (
        A
        ∣
        B
        )
        =
        
          
            
              P
              (
              B
              ∣
              A
              )
              P
              (
              A
              )
            
            
              P
              (
              B
              )
            
          
        
      
    
    {\\displaystyle P(A\\mid B)={{P(B\\mid A)P(A)} \\over {P(B)}}}
  
. Another option is to display conditional probabilities in a conditional probability table to illuminate the relationship between events.


== Definition ==


=== Conditioning on an event ===


==== Kolmogorov definition ====
Given two events A and B from the sigma-field of a probability space, with the unconditional probability of B being greater than zero (i.e., P(B) > 0), the conditional probability of A given B (
  
    
      
        P
        (
        A
        ∣
        B
        )
      
    
    {\\displaystyle P(A\\mid B)}
  
) is the probability of A occurring if B has or is assumed to have happened. A is assumed to be the set of all possible outcomes of an experiment or random trial that has a restricted or reduced sample space. The conditional probability can be found by the quotient of the probability of the joint intersection of events A and B, that is, 
  
    
      
        P
        (
        A
        ∩
        B
        )
      
    
    {\\displaystyle P(A\\cap B)}
  
, the probability at which A and B occur together, and the probability of B:

  
    
      
        P
        (
        A
        ∣
        B
        )
        =
        
          
            
              P
              (
              A
              ∩
              B
              )
            
            
              P
              (
              B
              )
            
          
        
        .
      
    
    {\\displaystyle P(A\\mid B)={\\frac {P(A\\cap B)}{P(B)}}.}
  

For a sample space consisting of equal likelihood outcomes, the probability of the event A is understood as the fraction of the number of outcomes in A to the number of all outcomes in the sample space. Then, this equation is understood as the fraction of the set 
  
    
      
        A
        ∩
        B
      
    
    {\\displaystyle A\\cap B}
  
 to the set B. Note that the above equation is a definition, not just a theoretical result. We denote the quantity 
  
    
      
        
          
            
              P
              (
              A
              ∩
              B
              )
            
            
              P
              (
              B
              )
            
          
        
      
    
    {\\displaystyle {\\frac {P(A\\cap B)}{P(B)}}}
  
 as 
  
    
      
        P
        (
        A
        ∣
        B
        )
      
    
    {\\displaystyle P(A\\mid B)}
  
 and call it the "conditional probability of A given B."


==== As an axiom of probability ====
Some authors, such as de Finetti, prefer to introduce conditional probability as an axiom of probability:

  
    
      
        P
        (
        A
        ∩
        B
        )
        =
        P
        (
        A
        ∣
        B
        )
        P
        (
        B
        )
        .
      
    
    {\\displaystyle P(A\\cap B)=P(A\\mid B)P(B).}
  

This equation for a conditional probability, although mathematically equivalent, may be intuitively easier to understand. It can be interpreted as "the probability of B occurring multiplied by the probability of A occurring, provided that B has occurred, is equal to the probability of the A and B occurrences together, although not necessarily occurring at the same time". Additionally, this may be preferred philosophically; under major probability interpretations, such as the subjective theory, conditional probability is considered a primitive entity.""",
    tier=3,
    domain="probability",
    source="Wikipedia, 'Conditional probability'",
    source_url="https://en.wikipedia.org/wiki/Conditional_probability",
))

register_atom(Atom(
    atom_type="theorem",
    name="bayes_theorem",
    content="""Bayes' theorem (alternatively Bayes' law or Bayes' rule), named after Thomas Bayes (), gives a mathematical rule for inverting conditional probabilities, allowing the probability of a cause to be found given its effect. For example, with Bayes' theorem, the probability that a patient has a disease given that they tested positive for that disease can be found using the probability that the test yields a positive result when the disease is present. The theorem was developed in the 18th century by Bayes and independently by Pierre-Simon Laplace.
One of Bayes' theorem's many applications is Bayesian inference, an approach to statistical inference, where it is used to invert the probability of observations given a model configuration (i.e., the likelihood function) to obtain the probability of the model configuration given the observations (i.e., the posterior probability).


== History ==
Bayes' theorem is named after Thomas Bayes, a minister, statistician, and philosopher. Bayes used conditional probability to provide an algorithm (his Proposition 9) that uses evidence to calculate limits on an unknown parameter. His work was published in 1763 as An Essay Towards Solving a Problem in the Doctrine of Chances. Bayes studied how to compute a distribution for the probability parameter of a binomial distribution (in modern terminology). After Bayes's death, his family gave his papers to a friend, the minister, philosopher, and mathematician Richard Price.
Price significantly edited the unpublished manuscript for two years before sending it to a friend who read it aloud at the Royal Society on 23 December 1763. Price edited Bayes's major work "An Essay Towards Solving a Problem in the Doctrine of Chances" (1763), which appeared in Philosophical Transactions, and contains Bayes' theorem. Price wrote an introduction to the paper that provides some of the philosophical basis of Bayesian statistics and chose one of the two solutions Bayes offered. In 1765, Price was elected a Fellow of the Royal Society in recognition of his work on Bayes's legacy. On 27 April, a letter sent to his friend Benjamin Franklin was read out at the Royal Society, and later published, in which Price applies this work to population and computing 'life-annuities'.
Independently of Bayes, Pierre-Simon Laplace used conditional probability to formulate the relation of an updated posterior probability from a prior probability, given evidence. He reproduced and extended Bayes's results in 1774, apparently unaware of Bayes's work, and summarized his results in Théorie analytique des probabilités (1812). The Bayesian interpretation of probability was developed mainly by Laplace.
About 200 years later, Sir Harold Jeffreys put Bayes's algorithm and Laplace's formulation on an axiomatic basis, writing in a 1973 book that Bayes' theorem "is to the theory of probability what the Pythagorean theorem is to geometry".
Stephen Stigler used a Bayesian argument to conclude that Bayes' theorem was discovered by Nicholas Saunderson, a blind English mathematician, some time before Bayes, but that is disputed. F. Thomas Bruss reviewed Bayes's "An essay towards solving a problem in the doctrine of chances" as communicated by Price. He agreed with Stigler's analysis on many points, but not on the question of priority. Bruss underlined the intuitive part of Bayes's formula and added independent arguments about Bayes's probable motivation for his work. He concluded that, unless the contrary is proven, the name "Bayes' Theorem" or "Bayes' formula" is justifiable.
Martyn Hooper and Sharon McGrayne have argued that Price's contribution was substantial:

By modern standards, we should refer to the Bayes–Price rule. Price discovered Bayes's work, recognized its importance, corrected it, contributed to the article, and found a use for it. The modern convention of employing Bayes's name alone is unfair but so entrenched that anything else makes little sense.
The "Bayes factor" or "likelihood" that appears when writing Bayes' theorem in odds form appears in the early 1940s work of Alan Turing, who called it the "factor in favour of a proposition". In 1878, Charles Sanders Peirce used the logarithm of this factor as the "weight of evidence" for a proposition.


== Statement of theorem ==
Bayes' theorem is stated mathematically as the following equation:

where 
  
    
      
        A
      
    
    {\\displaystyle A}
  
 and 
  
    
      
        B
      
    
    {\\displaystyle B}
  
 are events and 
  
    
      
        P
        (
        B
        )
        ≠
        0
      
    
    {\\displaystyle P(B)\\neq 0}
  
.

  
    
      
        P
        (
        A
        |
        B
        )
      
    
    {\\displaystyle P(A\\vert B)}
  
 is a conditional probability: the probability of event 
  
    
      
        A
      
    
    {\\displaystyle A}
  
 occurring given that 
  
    
      
        B
      
    
    {\\displaystyle B}
  
 is true. It is also called the posterior probability of 
  
    
      
        A
      
    
    {\\displaystyle A}
  
 given 
  
    
      
        B
      
    
    {\\displaystyle B}
  
.

  
    
      
        P
        (
        B
        |
        A
        )
      
    
    {\\displaystyle P(B\\vert A)}
  
 is also a conditional probability: the probability of event 
  
    
      
        B
      
    
    {\\displaystyle B}
  
 occurring given that 
  
    
      
        A
      
    
    {\\displaystyle A}
  
 is true. It can also be interpreted as the likelihood function evaluated at 
  
    
      
        A
      
    
    {\\displaystyle A}
  
 given a fixed 
  
    
      
        B
      
    
    {\\displaystyle B}
  
.

  
    
      
        P
        (
        A
        )
      
    
    {\\displaystyle P(A)}
  
 and 
  
    
      
        P
        (
        B
        )
      
    
    {\\displaystyle P(B)}
  
 are the probabilities of observing 
  
    
      
        A
      
    
    {\\displaystyle A}
  
 and 
  
    
      
        B
      
    
    {\\displaystyle B}
  
 respectively without any given conditions. 
  
    
      
        P
        (
        A
        )
      
    
    {\\displaystyle P(A)}
  
, the quantity of interest, is often called 'the prior probability' (prior to new evidence). Technically both 
  
    
      
        P
        (
        A
        )
      
    
    {\\displaystyle P(A)}
  
 and 
  
    
      
        P
        (
        B
        )
      
    
    {\\displaystyle P(B)}
  
 could be called prior, unconditioned, or marginal probabilities.

Bayes' theorem may be derived from the relation between joint and conditional probabilities.""",
    tier=4,
    domain="probability",
    source="Wikipedia, 'Bayes' theorem'",
    source_url="https://en.wikipedia.org/wiki/Bayes%27_theorem",
))

register_atom(Atom(
    atom_type="formula",
    name="expected_value",
    content="""In probability theory, the expected value (also called expectation, mean, or first moment) is a generalization of the weighted average.
The expected value of a random variable with a finite number of outcomes is a weighted average of all possible outcomes. In the case of a continuum of possible outcomes, the expectation is defined by integration. In the axiomatic foundation for probability provided by measure theory, the expectation is given by Lebesgue integration.
The expected value of a random variable X is often denoted by 
  
    
      
        
          E
        
        (
        X
        )
      
    
    {\\displaystyle {\\text{E}}(X)}
  
, 
  
    
      
        
          E
        
        [
        X
        ]
      
    
    {\\displaystyle {\\text{E}}[X]}
  
, or 
  
    
      
        
          E
        
        X
      
    
    {\\displaystyle {\\text{E}}X}
  
, with E also often stylized as 
  
    
      
        
          E
        
      
    
    {\\displaystyle \\mathbb {E} }
  
, 
  
    
      
        
          
            E
          
        
      
    
    {\\displaystyle {\\mathcal {E}}}
  
 or E.


== History ==
The concept of expected value emerged in the mid-17th century from the "problem of points", a puzzle centered on how to fairly divide stakes between two players forced to end a game prematurely. While the problem had been debated for centuries, it gained new momentum in 1654 when the Chevalier de Méré, a French writer and amateur mathematician, presented it to Blaise Pascal. Méré claimed that this problem could not be solved and that it showed just how flawed mathematics was when it came to its application to the real world. Pascal, being a mathematician, decided to work on a solution to the problem.
He began to discuss the problem in the famous series of letters to Pierre de Fermat. Soon enough, they both independently came up with a solution. They solved the problem in different computational ways, but their results were identical because their computations were based on the same fundamental principle. The principle is that the value of a future gain should be directly proportional to the chance of getting it. This principle seemed to have come naturally to both of them. They were very pleased by the fact that they had found essentially the same solution, and this in turn made them absolutely convinced that they had solved the problem conclusively; however, they did not publish their findings. They only informed a small circle of mutual scientific friends in Paris about it.
In Dutch mathematician Christiaan Huygens' book, he considered the problem of points, and presented a solution based on the same principle as the solutions of Pascal and Fermat. Huygens published his treatise in 1657, (see Huygens (1657)) "De ratiociniis in ludo aleæ" on probability theory just after visiting Paris. The book extended the concept of expectation by adding rules for how to calculate expectations in more complicated situations than the original problem (e.g., for three or more players), and can be seen as the first successful attempt at laying down the foundations of the theory of probability.
In the foreword to his treatise, Huygens wrote:

It should be said, also, that for some time some of the best mathematicians of France have occupied themselves with this kind of calculus so that no one should attribute to me the honour of the first invention. This does not belong to me. But these savants, although they put each other to the test by proposing to each other many questions difficult to solve, have hidden their methods. I have had therefore to examine and go deeply for myself into this matter by beginning with the elements, and it is impossible for me for this reason to affirm that I have even started from the same principle. But finally I have found that my answers in many cases do not differ from theirs.
In the mid-nineteenth century, Pafnuty Chebyshev became the first person to think systematically in terms of the expectations of random variables.


=== Etymology ===
Neither Pascal nor Huygens used the term "expectation" in its modern sense. In particular, Huygens writes:

That any one Chance or Expectation to win any thing is worth just such a Sum, as wou'd procure in the same Chance and Expectation at a fair Lay. ... If I expect a or b, and have an equal chance of gaining them, my Expectation is worth (a+b)/2.
More than a hundred years later, in 1814, Pierre-Simon Laplace published his tract "Théorie analytique des probabilités", where the concept of expected value was defined explicitly:

... this advantage in the theory of chance is the product of the sum hoped for by the probability of obtaining it; it is the partial sum which ought to result when we do not wish to run the risks of the event in supposing that the division is made proportional to the probabilities. This division is the only equitable one when all strange circumstances are eliminated; because an equal degree of probability gives an equal right for the sum hoped for. We will call this advantage mathematical hope.


== Notations ==
The use of the letter E to denote "expected value" goes back to W. A. Whitworth in 1901. The symbol has since become popular for English writers. In German, E stands for Erwartungswert, in Spanish for esperanza matemática, and in French for espérance mathématique.
When "E" is used to denote "expected value", authors use a variety of stylizations: the expectation operator can be stylized as E (upright), E (italic), or 
  
    
      
        
          E
        
      
    
    {\\displaystyle \\mathbb {E} }
  
 (in blackboard bold), while a variety of bracket notations (such as E(X), E[X], and EX) are all used.
Another popular notation is μX. ⟨X⟩, ⟨X⟩av, and 
  
    
      
        
          
            X
            ¯
          
        
      
    
    {\\displaystyle {\\overline {X}}}
  
 are commonly used in physics. M(X) is used in Russian-language literature.


== Definition ==
As discussed above, there are several context-dependent ways of defining the expected value. The simplest and original definition deals with the case of finitely many possible outcomes, such as in the flip of a coin. With the theory of infinite series, this can be extended to the case of countably many possible outcomes. It is also very common to consider the distinct case of random variables dictated by (piecewise-)continuous probability density functions, as these arise in many natural contexts. All of these specific definitions may be viewed as special cases of the general definition based upon the mathematical tools of measure theory and Lebesgue integration, which provide these different contexts with an axiomatic foundation and common language.
Any definition of expected value may be extended to define an expected value of a multidimensional random variable, i.e. a random vector 
  
    
      
        X
      
    
    {\\displaystyle X}
  
. It is defined component by component, as 
  
    
      
        E
        [
        X
        
          ]
          
            i
          
        
        =
        E
        [
        
          X
          
            i
          
        
        ]
      
    
    {\\displaystyle E[X]_{i}=E[X_{i}]}
  
.""",
    tier=3,
    domain="probability",
    source="Wikipedia, 'Expected value'",
    source_url="https://en.wikipedia.org/wiki/Expected_value",
))

register_atom(Atom(
    atom_type="result",
    name="binomial_dist",
    content="""In probability theory and statistics, the binomial distribution with parameters n and p is the discrete probability distribution of the number of successes in a sequence of n independent experiments, each asking a yes–no question, and each with its own Boolean-valued outcome: success (with probability p) or failure (with probability q = 1 − p). A single success/failure experiment is also called a Bernoulli trial or Bernoulli experiment, and a sequence of outcomes is called a Bernoulli process. For a single trial, that is, when n = 1, the binomial distribution is a Bernoulli distribution. The binomial distribution is the basis for the binomial test of statistical significance.
The binomial distribution is frequently used to model the number of successes in a sample of size n drawn with replacement from a population of size N. If the sampling is carried out without replacement, the draws are not independent and so the resulting distribution is a hypergeometric distribution, not a binomial one.  However, for N much larger than n, the binomial distribution remains a good approximation, and is widely used.


== Definitions ==


=== Probability mass function ===
If the random variable X follows the binomial distribution with parameters 
  
    
      
        n
        ∈
        
          N
        
      
    
    {\\displaystyle n\\in \\mathbb {N} }
  
 (a natural number) and p ∈ [0, 1], we write X ~ B(n, p). The probability of getting exactly k successes in n independent Bernoulli trials (with the same rate p) is given by the probability mass function:

  
    
      
        f
        (
        k
        ,
        n
        ,
        p
        )
        =
        Pr
        (
        X
        =
        k
        )
        =
        
          
            
              (
            
            
              n
              k
            
            
              )
            
          
        
        
          p
          
            k
          
        
        (
        1
        −
        p
        
          )
          
            n
            −
            k
          
        
      
    
    {\\displaystyle f(k,n,p)=\\Pr(X=k)={\\binom {n}{k}}p^{k}(1-p)^{n-k}}
  

for k = 0, 1, 2, ..., n, where

  
    
      
        
          
            
              (
            
            
              n
              k
            
            
              )
            
          
        
        =
        
          
            
              n
              !
            
            
              k
              !
              (
              n
              −
              k
              )
              !
            
          
        
      
    
    {\\displaystyle {\\binom {n}{k}}={\\frac {n!}{k!(n-k)!}}}
  

is the binomial coefficient. The formula can be understood as follows: pk qn−k is the probability of obtaining the sequence of n independent Bernoulli trials in which k trials are "successes" and the remaining n − k trials are "failures". Since the trials are independent with probabilities remaining constant between them, any sequence of n trials with k successes (and n − k failures) has the same probability of being achieved (regardless of positions of successes within the sequence). There are 
  
    
      
        
          
            
              (
            
            
              n
              k
            
            
              )
            
          
        
      
    
    {\\textstyle {\\binom {n}{k}}}
  
 such sequences, since the binomial coefficient 
  
    
      
        
          
            
              (
            
            
              n
              k
            
            
              )
            
          
        
      
    
    {\\textstyle {\\binom {n}{k}}}
  
 counts the number of ways to choose the positions of the k successes among the n trials. The binomial distribution is concerned with the probability of obtaining any of these sequences, meaning the probability of obtaining one of them (pk qn−k) must be added 
  
    
      
        
          
            
              (
            
            
              n
              k
            
            
              )
            
          
        
      
    
    {\\textstyle {\\binom {n}{k}}}
  
 times, hence 
  
    
      
        Pr
        (
        X
        =
        k
        )
        =
        
          
            
              (
            
            
              n
              k
            
            
              )
            
          
        
        
          p
          
            k
          
        
        (
        1
        −
        p
        
          )
          
            n
            −
            k
          
        
      
    
    {\\textstyle \\Pr(X=k)={\\binom {n}{k}}p^{k}(1-p)^{n-k}}
  
.
In creating reference tables for binomial distribution probability, usually, the table is filled in up to n / 2 values. This is because for k > n/2, the probability can be calculated by its complement as

  
    
      
        f
        (
        k
        ,
        n
        ,
        p
        )
        =
        f
        (
        n
        −
        k
        ,
        n
        ,
        1
        −
        p
        )
        .
      
    
    {\\displaystyle f(k,n,p)=f(n-k,n,1-p).}
  

Looking at the expression f(k, n, p) as a function of k, there is a k value that maximizes it. This k value can be found by calculating

  
    
      
        
          
            
              f
              (
              k
              +
              1
              ,
              n
              ,
              p
              )
            
            
              f
              (
              k
              ,
              n
              ,
              p
              )
            
          
        
        =
        
          
            
              (
              n
              −
              k
              )
              p
            
            
              (
              k
              +
              1
              )
              (
              1
              −
              p
              )
            
          
        
      
    
    {\\displaystyle {\\frac {f(k+1,n,p)}{f(k,n,p)}}={\\frac {(n-k)p}{(k+1)(1-p)}}}
  

and comparing it to 1. There is always an integer M that satisfies

  
    
      
        (
        n
        +
        1
        )
        p
        −
        1
        ≤
        M
        <
        (
        n
        +
        1
        )
        p
        .
      
    
    {\\displaystyle (n+1)p-1\\leq M<(n+1)p.}
  

f(k, n, p) is monotone increasing for k < M and monotone decreasing for k > M, with the exception of the case where (n + 1)p is an integer. In this case, there are two values for which f is maximal: (n + 1)p and (n + 1)p − 1. M is the most probable outcome (that is, the most likely, although this can still be unlikely overall) of the Bernoulli trials and is called the mode.


=== Example ===
Suppose a biased coin comes up heads with probability 0.3 when tossed.""",
    tier=5,
    domain="probability",
    source="Wikipedia, 'Binomial distribution'",
    source_url="https://en.wikipedia.org/wiki/Binomial_distribution",
))

register_atom(Atom(
    atom_type="formula",
    name="poisson_dist",
    content="""In probability theory and statistics, the Poisson distribution () is a discrete probability distribution that expresses the probability of a given number of events occurring in a fixed interval of time if these events occur with a known constant mean rate and independently of the time since the last event. It can also be used for the number of events in other types of intervals than time, and in dimension greater than 1 (e.g., number of events in a given area or volume).
The Poisson distribution is named after French mathematician Siméon Denis Poisson. It plays an important role for discrete-stable distributions.
Under a Poisson distribution with the expectation of λ events in a given interval, the probability of k events in the same interval is:

  
    
      
        
          
            
              
                λ
                
                  k
                
              
              
                e
                
                  −
                  λ
                
              
            
            
              k
              !
            
          
        
        .
      
    
    {\\displaystyle {\\frac {\\lambda ^{k}e^{-\\lambda }}{k!}}.}
  

For instance, consider a call center which receives an average of λ = 3 calls per minute at all times of day. If the number of calls received in any two given disjoint time intervals is independent, then the number k of calls received during any minute has a Poisson probability distribution. Receiving  k = 1 to 4 calls then has a probability of about 0.77, while receiving 0 or at least 5 calls has a probability of about 0.23.
A classic example used to motivate the Poisson distribution is the number of radioactive decay events during a fixed observation period.


== History ==
The introduction of the Poisson distribution is credited to French mathematician and physicist Siméon Denis Poisson (1781–1840), who published it together with his probability theory in Recherches sur la probabilité des jugements en matière criminelle et en matière civile (1837). This work theorizes about the number of wrongful convictions in a given country by focusing on certain random variables N that count the number of events that take place during a time interval of given length. However, similar results had already been given in 1711 by Abraham de Moivre in De Mensura Sortis seu; de Probabilitate Eventuum in Ludis a Casu Fortuito Pendentibus . This makes it an example of Stigler's law and it has prompted some authors to argue that the Poisson distribution should bear the name of de Moivre.
In 1860, Simon Newcomb fitted the Poisson distribution to the number of stars found in a unit of space.
A further practical application was made by Ladislaus Bortkiewicz in 1898. Bortkiewicz showed that the frequency with which soldiers in the Prussian army were accidentally killed by horse kicks could be well modeled by a Poisson distribution..


== Definitions ==


=== Probability mass function ===
A discrete random variable X is said to have a Poisson distribution with parameter 
  
    
      
        λ
        >
        0
      
    
    {\\displaystyle \\lambda >0}
  
 if it has a probability mass function given by:

  
    
      
        f
        (
        k
        ;
        λ
        )
        =
        Pr
        (
        X
        
          =
        
        k
        )
        =
        
          
            
              
                λ
                
                  k
                
              
              
                e
                
                  −
                  λ
                
              
            
            
              k
              !
            
          
        
        ,
      
    
    {\\displaystyle f(k;\\lambda )=\\Pr(X{=}k)={\\frac {\\lambda ^{k}e^{-\\lambda }}{k!}},}
  

where

k is the number of occurrences (
  
    
      
        k
        =
        0
        ,
        1
        ,
        2
        ,
        …
      
    
    {\\displaystyle k=0,1,2,\\ldots }
  
)
e is Euler's number (
  
    
      
        e
        =
        2.71828
        …
      
    
    {\\displaystyle e=2.71828\\ldots }
  
)
k! = k(k–1) ··· (3)(2)(1) is the factorial.
The positive real number λ is equal to the expected value of X and also to its variance.

  
    
      
        λ
        =
        E
        ⁡
        (
        X
        )
        =
        Var
        ⁡
        (
        X
        )
        .
      
    
    {\\displaystyle \\lambda =\\operatorname {E} (X)=\\operatorname {Var} (X).}
  

The Poisson distribution can be applied to systems with a large number of possible events, each of which is rare. The number of such events that occur during a fixed time interval is, under the right circumstances, a random number with a Poisson distribution.
The equation can be adapted if, instead of the average number of events 
  
    
      
        λ
        ,
      
    
    {\\displaystyle \\lambda ,}
  
 we are given the average rate 
  
    
      
        r
      
    
    {\\displaystyle r}
  
 at which events occur.""",
    tier=5,
    domain="probability",
    source="Wikipedia, 'Poisson distribution'",
    source_url="https://en.wikipedia.org/wiki/Poisson_distribution",
))

register_atom(Atom(
    atom_type="formula",
    name="variance_dist",
    content="""In probability theory and statistics, variance is the expected value of the squared deviation from the mean of a random variable. The standard deviation is obtained as the square root of the variance. Variance is a measure of dispersion, meaning it is a measure of how far a set of numbers are spread out from their average value. It is the second central moment of a distribution, and the covariance of the random variable with itself, and it is often represented by ⁠
  
    
      
        
          σ
          
            2
          
        
      
    
    {\\displaystyle \\sigma ^{2}}
  
⁠, ⁠
  
    
      
        
          s
          
            2
          
        
      
    
    {\\displaystyle s^{2}}
  
⁠, ⁠
  
    
      
        Var
        ⁡
        (
        X
        )
      
    
    {\\displaystyle \\operatorname {Var} (X)}
  
⁠, ⁠
  
    
      
        V
        (
        X
        )
      
    
    {\\displaystyle V(X)}
  
⁠, or ⁠
  
    
      
        
          V
        
        (
        X
        )
      
    
    {\\displaystyle \\mathbb {V} (X)}
  
⁠.
An advantage of variance as a measure of dispersion is that it is more amenable to algebraic manipulation than other measures of dispersion such as the expected absolute deviation; for example, the variance of a sum of uncorrelated random variables is equal to the sum of their variances. A disadvantage of the variance for practical applications is that, unlike the standard deviation, its units differ from the random variable, which is why the standard deviation is more commonly reported as a measure of dispersion once the calculation is finished. Another disadvantage is that the variance is not finite for many distributions.
There are two distinct concepts that are both called "variance". One, as discussed above, is part of a theoretical probability distribution and is defined by an equation. The other variance is a characteristic of a set of observations. When variance is calculated from observations, those observations are typically measured from a real-world system. If all possible observations of the system are present, then the calculated variance is called the population variance. Normally, however, only a subset is available, and the variance calculated from this is called the sample variance. The variance calculated from a sample is considered an estimate of the full population variance. There are multiple ways to estimate the population variance on the basis of the sample variance, as discussed in the section below.
The two kinds of variance are closely related. To see how, consider that a theoretical probability distribution can be used as a generator of hypothetical observations. If an infinite number of observations are generated using a distribution, then the sample variance calculated from that infinite set will match the value calculated using the distribution's equation for variance. Variance has a central role in statistics, where some ideas that use it include descriptive statistics, statistical inference, hypothesis testing, goodness of fit, and Monte Carlo sampling.


== Definition ==
The variance of a random variable 
  
    
      
        X
      
    
    {\\displaystyle X}
  
 is the expected value of the squared deviation from the mean of ⁠
  
    
      
        X
      
    
    {\\displaystyle X}
  
⁠, ⁠
  
    
      
        μ
        =
        E
        ⁡
        [
        X
        ]
      
    
    {\\displaystyle \\mu =\\operatorname {E} [X]}
  
⁠:

  
    
      
        Var
        ⁡
        (
        X
        )
        =
        E
        ⁡
        
          [
          
            (
            X
            −
            μ
            
              )
              
                2
              
            
          
          ]
        
        .
      
    
    {\\displaystyle \\operatorname {Var} (X)=\\operatorname {E} \\left[(X-\\mu )^{2}\\right].}
  

This definition encompasses random variables that are generated by processes that are discrete, continuous, neither, or mixed. The variance can also be thought of as the covariance of a random variable with itself:

  
    
      
        Var
        ⁡
        (
        X
        )
        =
        Cov
        ⁡
        (
        X
        ,
        X
        )
        .
      
    
    {\\displaystyle \\operatorname {Var} (X)=\\operatorname {Cov} (X,X).}
  

The variance is also equivalent to the second cumulant of a probability distribution that generates ⁠
  
    
      
        X
      
    
    {\\displaystyle X}
  
⁠. The variance is typically designated as ⁠
  
    
      
        Var
        ⁡
        (
        X
        )
      
    
    {\\displaystyle \\operatorname {Var} (X)}
  
⁠, or sometimes as 
  
    
      
        V
        (
        X
        )
      
    
    {\\displaystyle V(X)}
  
 or ⁠
  
    
      
        
          V
        
        (
        X
        )
      
    
    {\\displaystyle \\mathbb {V} (X)}
  
⁠, or symbolically as ⁠
  
    
      
        
          σ
          
            X
          
          
            2
          
        
      
    
    {\\displaystyle \\sigma _{X}^{2}}
  
⁠ or simply 
  
    
      
        
          σ
          
            2
          
        
      
    
    {\\displaystyle \\sigma ^{2}}
  
 (pronounced "sigma squared").""",
    tier=4,
    domain="probability",
    source="Wikipedia, 'Variance'",
    source_url="https://en.wikipedia.org/wiki/Variance",
))

register_atom(Atom(
    atom_type="theorem",
    name="total_probability",
    content="""In probability theory, the law (or formula) of total probability is a fundamental rule relating marginal probabilities to conditional probabilities. It expresses the total probability of an outcome which can be realized via several distinct events, hence the name.


== Statement ==
The law of total probability is a theorem that states, in its discrete case, if 
  
    
      
        
          {
          
            
              B
              
                n
              
            
            :
            n
            =
            1
            ,
            2
            ,
            3
            ,
            …
          
          }
        
      
    
    {\\displaystyle \\left\\{{B_{n}:n=1,2,3,\\ldots }\\right\\}}
  
 is a finite or countably infinite set of mutually exclusive and collectively exhaustive events, then for any event 
  
    
      
        A
      
    
    {\\displaystyle A}
  

  
    
      
        P
        (
        A
        )
        =
        
          ∑
          
            n
          
        
        P
        (
        A
        ∩
        
          B
          
            n
          
        
        )
      
    
    {\\displaystyle P(A)=\\sum _{n}P(A\\cap B_{n})}
  

or, alternatively,

  
    
      
        P
        (
        A
        )
        =
        
          ∑
          
            n
          
        
        P
        (
        A
        ∣
        
          B
          
            n
          
        
        )
        P
        (
        
          B
          
            n
          
        
        )
        ,
      
    
    {\\displaystyle P(A)=\\sum _{n}P(A\\mid B_{n})P(B_{n}),}
  

where, for any 
  
    
      
        n
      
    
    {\\displaystyle n}
  
, if 
  
    
      
        P
        (
        
          B
          
            n
          
        
        )
        =
        0
      
    
    {\\displaystyle P(B_{n})=0}
  
, then these terms are simply omitted from the summation since 
  
    
      
        P
        (
        A
        ∣
        
          B
          
            n
          
        
        )
      
    
    {\\displaystyle P(A\\mid B_{n})}
  
 is finite.
The summation can be interpreted as a weighted average, and consequently the marginal probability, 
  
    
      
        P
        (
        A
        )
      
    
    {\\displaystyle P(A)}
  
, is sometimes called "average probability"; "overall probability" is sometimes used in less formal writings.
The law of total probability can also be stated for conditional probabilities: 

  
    
      
        
          
            
              
                P
                (
                
                  A
                  ∣
                  C
                
                )
              
              
                
                =
                
                  
                    
                      P
                      (
                      
                        A
                        ,
                        C
                      
                      )
                    
                    
                      P
                      (
                      C
                      )
                    
                  
                
                =
                
                  
                    
                      
                        ∑
                        
                          n
                        
                      
                      
                        P
                        (
                        
                          A
                          ,
                          
                            
                              B
                              
                                n
                              
                            
                          
                          ,
                          C
                        
                        )
                      
                    
                    
                      P
                      (
                      C
                      )
                    
                  
                
              
            
            
              
              
                
                =
                
                  
                    
                      
                        ∑
                        
                          n
                        
                      
                      P
                      (
                      
                        A
                        ∣
                        
                          
                            B
                            
                              n
                            
                          
                        
                        ,
                        C
                      
                      )
                      P
                      (
                      
                        
                          
                            B
                            
                              n
                            
                          
                        
                        ∣
                        C
                      
                      )
                      P
                      (
                      C
                      )
                    
                    
                      P
                      (
                      C
                      )
                    
                  
                
              
            
            
              
              
                
                =
                
                  ∑
                  
                    n
                  
                
                P
                (
                
                  A
                  ∣
                  
                    
                      B
                      
                        n
                      
                    
                  
                  ,
                  C
                
                )
                P
                (
                
                  
                    
                      B
                      
                        n
                      
                    
                  
                  ∣
                  C
                
                )
              
            
          
        
      
    
    {\\displaystyle {\\begin{aligned}P({A\\mid C})&={\\frac {P({A,C})}{P(C)}}={\\frac {\\sum \\limits _{n}{P({A,{B_{n}},C})}}{P(C)}}\\\\[2ex]&={\\frac {\\sum \\limits _{n}P({A\\mid {B_{n}},C})P({{B_{n}}\\mid C})P(C)}{P(C)}}\\\\[2ex]&=\\sum \\limits _{n}P({A\\mid {B_{n}},C})P({{B_{n}}\\mid C})\\end{aligned}}}
  

Taking the 
  
    
      
        
          B
          
            n
          
        
      
    
    {\\displaystyle B_{n}}
  
 as above, and assuming 
  
    
      
        C
      
    
    {\\displaystyle C}
  
 is an event independent of any of the 
  
    
      
        
          B
          
            n
          
        
      
    
    {\\displaystyle B_{n}}
  
:

  
    
      
        P
        (
        A
        ∣
        C
        )
        =
        
          ∑
          
            n
          
        
        P
        (
        A
        ∣
        C
        ,
        
          B
          
            n
          
        
        )
        P
        (
        
          B
          
            n
          
        
        )
      
    
    {\\displaystyle P(A\\mid C)=\\sum _{n}P(A\\mid C,B_{n})P(B_{n})}
  


== Continuous case ==
The law of total probability extends to the case of conditioning on events generated by continuous random variables.""",
    tier=4,
    domain="probability",
    source="Wikipedia, 'Law of total probability'",
    source_url="https://en.wikipedia.org/wiki/Law_of_total_probability",
))

register_atom(Atom(
    atom_type="definition",
    name="independence_test",
    content="""Independence is a fundamental notion in probability theory, as in statistics and the theory of stochastic processes. Two events are independent, statistically independent, or stochastically independent if, informally speaking, the occurrence of one does not affect the probability of occurrence of the other or, equivalently, does not affect the odds. Similarly, two random variables are independent if the realization of one does not affect the probability distribution of the other. Conversely, dependence is when the occurrence of one event does affect the likelihood of another.
When dealing with collections of more than two events, two notions of independence need to be distinguished. The events are called pairwise independent if any two events in the collection are independent of each other, while mutual independence (or collective independence) of events means, informally speaking, that each event is independent of any combination of other events in the collection. A similar notion exists for collections of random variables. Mutual independence implies pairwise independence, but not the other way around. In the standard literature of probability theory, statistics, and stochastic processes, independence without further qualification usually refers to mutual independence.


== Definition ==


=== For events ===


==== Two events ====
Two events 
  
    
      
        A
      
    
    {\\displaystyle A}
  
 and 
  
    
      
        B
      
    
    {\\displaystyle B}
  
 are independent (often written as 
  
    
      
        A
        ⊥
        B
      
    
    {\\displaystyle A\\perp B}
  
 or 
  
    
      
        A
        ⊥
        
        
        
        ⊥
        B
      
    
    {\\displaystyle A\\perp \\!\\!\\!\\perp B}
  
, where the latter symbol often is also used for conditional independence) if and only if their joint probability equals the product of their probabilities:

  
    
      
        A
        ∩
        B
        ≠
        ∅
      
    
    {\\displaystyle A\\cap B\\neq \\emptyset }
  
 indicates that two independent events 
  
    
      
        A
      
    
    {\\displaystyle A}
  
 and 
  
    
      
        B
      
    
    {\\displaystyle B}
  
 have common elements in their sample space so that they are not mutually exclusive (mutually exclusive if and only if (iff) 
  
    
      
        A
        ∩
        B
        =
        ∅
      
    
    {\\displaystyle A\\cap B=\\emptyset }
  
). Why this defines independence is made clear by rewriting with conditional probabilities 
  
    
      
        P
        (
        A
        ∣
        B
        )
        =
        
          
            
              P
              (
              A
              ∩
              B
              )
            
            
              P
              (
              B
              )
            
          
        
      
    
    {\\displaystyle P(A\\mid B)={\\frac {P(A\\cap B)}{P(B)}}}
  
 as the probability at which the event 
  
    
      
        A
      
    
    {\\displaystyle A}
  
 occurs provided that the event 
  
    
      
        B
      
    
    {\\displaystyle B}
  
 has or is assumed to have occurred:

  
    
      
        
          P
        
        (
        A
        ∩
        B
        )
        =
        
          P
        
        (
        A
        )
        
          P
        
        (
        B
        )
        
        ⟺
        
        
          P
        
        (
        A
        ∣
        B
        )
        =
        
          
            
              
                P
              
              (
              A
              ∩
              B
              )
            
            
              
                P
              
              (
              B
              )
            
          
        
        =
        
          P
        
        (
        A
        )
        .
      
    
    {\\displaystyle \\mathrm {P} (A\\cap B)=\\mathrm {P} (A)\\mathrm {P} (B)\\iff \\mathrm {P} (A\\mid B)={\\frac {\\mathrm {P} (A\\cap B)}{\\mathrm {P} (B)}}=\\mathrm {P} (A).}
  

and similarly

  
    
      
        
          P
        
        (
        A
        ∩
        B
        )
        =
        
          P
        
        (
        A
        )
        
          P
        
        (
        B
        )
        
        ⟺
        
        
          P
        
        (
        B
        ∣
        A
        )
        =
        
          
            
              
                P
              
              (
              A
              ∩
              B
              )
            
            
              
                P
              
              (
              A
              )
            
          
        
        =
        
          P
        
        (
        B
        )
        .
      
    
    {\\displaystyle \\mathrm {P} (A\\cap B)=\\mathrm {P} (A)\\mathrm {P} (B)\\iff \\mathrm {P} (B\\mid A)={\\frac {\\mathrm {P} (A\\cap B)}{\\mathrm {P} (A)}}=\\mathrm {P} (B).}
  

Thus, the occurrence of 
  
    
      
        B
      
    
    {\\displaystyle B}
  
 does not affect the probability of 
  
    
      
        A
      
    
    {\\displaystyle A}
  
, and vice versa. In other words, 
  
    
      
        A
      
    
    {\\displaystyle A}
  
 and 
  
    
      
        B
      
    
    {\\displaystyle B}
  
 are independent of each other. Although the derived expressions may seem more intuitive, they are not the preferred definition, as the conditional probabilities may be undefined if 
  
    
      
        
          P
        
        (
        A
        )
      
    
    {\\displaystyle \\mathrm {P} (A)}
  
 or 
  
    
      
        
          P
        
        (
        B
        )
      
    
    {\\displaystyle \\mathrm {P} (B)}
  
 are 0. Furthermore, the preferred definition makes clear by symmetry that when 
  
    
      
        A
      
    
    {\\displaystyle A}
  
 is independent of 
  
    
      
        B
      
    
    {\\displaystyle B}
  
, 
  
    
      
        B
      
    
    {\\displaystyle B}
  
 is also independent of 
  
    
      
        A
      
    
    {\\displaystyle A}
  
.


==== Odds ====
Stated in terms of odds, two events are independent if and only if the odds ratio of ⁠
  
    
      
        A
      
    
    {\\displaystyle A}
  
⁠ and ⁠
  
    
      
        B
      
    
    {\\displaystyle B}
  
⁠ is unity (1).""",
    tier=3,
    domain="probability",
    source="Wikipedia, 'Independence (probability theory)'",
    source_url="https://en.wikipedia.org/wiki/Independence_%28probability_theory%29",
))

register_atom(Atom(
    atom_type="formula",
    name="markov_chain",
    content="""In probability theory and statistics, a Markov chain or Markov process is a stochastic process describing a sequence of possible events in which the probability of each event depends only on the state attained in the previous event. Informally, this may be thought of as, "What happens next depends only on the state of affairs now." A countably infinite sequence, in which the chain moves state at discrete time steps, gives a discrete-time Markov chain (DTMC). A continuous-time process is called a continuous-time Markov chain (CTMC). Markov processes are named in honor of the Russian mathematician Andrey Markov.
Markov chains have many applications as statistical models of real-world processes. They provide the basis for general stochastic simulation methods known as Markov chain Monte Carlo, which are used for simulating sampling from complex probability distributions, and have found application in areas including Bayesian statistics, biology, chemistry, economics, finance, information theory, physics, signal processing, and speech processing.
The adjectives Markovian and Markov are used to describe something that is related to a Markov process.


== Principles ==


=== Definition ===
A Markov process is a stochastic process that satisfies the Markov property (sometimes characterized as "memorylessness"). In simpler terms, it is a process for which predictions can be made regarding future outcomes based solely on its present state and—most importantly—such predictions are just as good as the ones that could be made knowing the process's full history. In other words, conditional on the present state of the system, its future and past states are independent.
A Markov chain is a type of Markov process that has either a discrete state space or a discrete index set (often representing time), but the precise definition of a Markov chain varies. For example, it is common to define a Markov chain as a Markov process in either discrete or continuous time with a countable state space (thus regardless of the nature of time), but it is also common to define a Markov chain as having discrete time in either countable or continuous state space (thus regardless of the state space).


=== Types of Markov chains ===
The system's state space and time parameter index need to be specified. The following table gives an overview of the different instances of Markov processes for different levels of state space generality for both discrete and continuous time:

Note that there is no definitive agreement in the literature on the use of some of the terms that signify special cases of Markov processes. Usually the term "Markov chain" is reserved for a process with a discrete set of times, that is, a discrete-time Markov chain (DTMC), but a few authors use the term "Markov process" to refer to a continuous-time Markov chain (CTMC) without explicit mention. In addition, there are other extensions of Markov processes that are referred to as such but do not necessarily fall within any of these four categories (see Markov model). Moreover, the time index need not necessarily be real-valued; like with the state space, there are conceivable processes that move through index sets with other mathematical constructs. Notice that the general state space continuous-time Markov chain is general to such a degree that it has no designated term.
While the time parameter is usually discrete, the state space of a Markov chain does not have any generally agreed-on restrictions: the term may refer to a process on an arbitrary state space. However, many applications of Markov chains employ finite or countably infinite state spaces, which have a more straightforward statistical analysis. Besides time-index and state-space parameters, there are many other variations, extensions and generalizations (see Variations). For simplicity, most of this article concentrates on the discrete-time, discrete state-space case, unless mentioned otherwise.


=== Transitions ===
The changes of state of the system are called transitions. The probabilities associated with various state changes are called transition probabilities. The process is characterized by a state space, a transition matrix describing the probabilities of particular transitions, and an initial state (or initial distribution) across the state space. By convention, we assume all possible states and transitions have been included in the definition of the process, so there is always a next state, and the process does not terminate.
A discrete-time random process involves a system which is in a certain state at each step, with the state changing randomly between steps. The steps are often thought of as moments in time, but they can equally well refer to physical distance or any other discrete measurement. Formally, the steps are the integers or natural numbers, and the random process is a mapping of these to states. The Markov property states that the conditional probability distribution for the system at the next step (and in fact at all future steps) depends only on the current state of the system, and not additionally on the state of the system at previous steps.
Since the system changes randomly, it is generally impossible to predict with certainty the state of a Markov chain at a given point in the future. However, the statistical properties of the system's future can be predicted. In many applications, it is these statistical properties that are important.


== History ==
Andrey Markov studied Markov processes in the early 20th century, publishing his first paper on the topic in 1906. Markov processes in continuous time were discovered long before his work in the early 20th century in the form of the Poisson process. Markov was interested in studying an extension of independent random sequences, motivated by a disagreement with Pavel Nekrasov who claimed independence was necessary for the weak law of large numbers to hold. In his first paper on Markov chains, published in 1906, Markov showed that under certain conditions the average outcomes of the Markov chain would converge to a fixed vector of values, so proving a weak law of large numbers without the independence assumption, which had been commonly regarded as a requirement for such mathematical laws to hold. Markov later used Markov chains to study the distribution of vowels in Eugene Onegin, written by Alexander Pushkin, and proved a central limit theorem for such chains.
In 1912 Henri Poincaré studied Markov chains on finite groups with an aim to study card shuffling. Other early uses of Markov chains include a diffusion model, introduced by Paul and Tatyana Ehrenfest in 1907, and a branching process, introduced by Francis Galton and Henry William Watson in 1873, preceding the work of Markov. After the work of Galton and Watson, it was later revealed that their branching process had been independently discovered and studied around three decades earlier by Irénée-Jules Bienaymé. Starting in 1928, Maurice Fréchet became interested in Markov chains, eventually resulting in him publishing in 1938 a detailed study on Markov chains.
Andrey Kolmogorov developed in a 1931 paper a large part of the early theory of continuous-time Markov processes. Kolmogorov was partly inspired by Louis Bachelier's 1900 work on fluctuations in the stock market as well as Norbert Wiener's work on Einstein's model of Brownian movement. He introduced and studied a particular set of Markov processes known as diffusion processes, where he derived a set of differential equations describing the processes. Independent of Kolmogorov's work, Sydney Chapman derived in a 1928 paper an equation, now called the Chapman–Kolmogorov equation, in a less mathematically rigorous way than Kolmogorov, while studying Brownian movement. The differential equations are now called the Kolmogorov equations or the Kolmogorov–Chapman equations.""",
    tier=5,
    domain="probability",
    source="Wikipedia, 'Markov chain'",
    source_url="https://en.wikipedia.org/wiki/Markov_chain",
))

register_atom(Atom(
    atom_type="formula",
    name="complex_arithmetic",
    content="""In mathematics, a complex number is an element of a number system that extends the real numbers with a specific element denoted i, called the imaginary unit and satisfying the equation 
  
    
      
        
          i
          
            2
          
        
        =
        −
        1
      
    
    {\\displaystyle i^{2}=-1}
  
; because no real number satisfies the above equation, i was called an imaginary number by René Descartes. Every complex number can be expressed in the form 
  
    
      
        a
        +
        b
        i
      
    
    {\\displaystyle a+bi}
  
, where a and b are real numbers, a is called the real part, and b is called the imaginary part. The set of complex numbers is denoted by either of the symbols 
  
    
      
        
          C
        
      
    
    {\\displaystyle \\mathbb {C} }
  
 or C. Despite the historical nomenclature, "imaginary" complex numbers have a mathematical existence as firm as that of the real numbers, and they are fundamental tools in the scientific description of the natural world.
Complex numbers allow solutions to all polynomial equations, even those that have no solutions in real numbers. More precisely, the fundamental theorem of algebra asserts that every non-constant polynomial equation with real or complex coefficients has a solution which is a complex number. For example, the equation

  
    
      
        (
        x
        +
        1
        
          )
          
            2
          
        
        =
        −
        9
      
    
    {\\displaystyle (x+1)^{2}=-9}
  

has no real solution, because the square of a real number cannot be negative, but has the two nonreal complex solutions 
  
    
      
        x
        =
        −
        1
        +
        3
        i
      
    
    {\\displaystyle x=-1+3i}
  
 and 
  
    
      
        x
        =
        −
        1
        −
        3
        i
      
    
    {\\displaystyle x=-1-3i}
  
.
Addition, subtraction and multiplication of complex numbers are defined, taking advantage of the rule 
  
    
      
        
          i
          
            2
          
        
        =
        −
        1
      
    
    {\\displaystyle i^{2}=-1}
  
, along with the associative, commutative, and distributive laws. Every nonzero complex number has a multiplicative inverse, allowing division by complex numbers other than zero. This makes the complex numbers a field with the real numbers as a subfield. Because of these properties, ⁠
  
    
      
        a
        +
        b
        i
        =
        a
        +
        i
        b
      
    
    {\\displaystyle a+bi=a+ib}
  
⁠, and which form is written depends upon convention and style considerations.
The complex numbers also form a real vector space of dimension two, with 
  
    
      
        {
        1
        ,
        i
        }
      
    
    {\\displaystyle \\{1,i\\}}
  
 as a standard basis. This standard basis makes the complex numbers a Cartesian plane, called the complex plane. This allows a geometric interpretation of the complex numbers and their operations, and conversely some geometric objects and operations can be expressed in terms of complex numbers. For example, the real numbers form the real line, which is pictured as the horizontal axis of the complex plane, while real multiples of 
  
    
      
        i
      
    
    {\\displaystyle i}
  
 are the vertical axis. A complex number can also be defined by its geometric polar coordinates: the radius is called the absolute value of the complex number, while the angle from the positive real axis is called the argument of the complex number. The complex numbers of absolute value one form the unit circle. Adding a fixed complex number to all complex numbers defines a translation in the complex plane, and multiplying by a fixed complex number is a similarity centered at the origin (dilating by the absolute value, and rotating by the argument). The operation of complex conjugation is the reflection symmetry with respect to the real axis. 
The complex numbers form a rich structure that is simultaneously an algebraically closed field, a commutative algebra over the reals, and a Euclidean vector space of dimension two. 


== Definition and basic operations ==

A complex number is an expression of the form a + bi, where a and b are real numbers, and i is an abstract symbol, the so-called imaginary unit, whose meaning will be explained further below. For example, 2 + 3i is a complex number.
For a complex number a + bi, the real number a is called its real part, and the real number b (not the complex number bi) is its imaginary part. The real part of a complex number z is denoted Re(z), 
  
    
      
        
          
            R
            e
          
        
        (
        z
        )
      
    
    {\\displaystyle {\\mathcal {Re}}(z)}
  
, or 
  
    
      
        
          
            R
          
        
        (
        z
        )
      
    
    {\\displaystyle {\\mathfrak {R}}(z)}
  
; the imaginary part is Im(z), 
  
    
      
        
          
            I
            m
          
        
        (
        z
        )
      
    
    {\\displaystyle {\\mathcal {Im}}(z)}
  
, or 
  
    
      
        
          
            I
          
        
        (
        z
        )
      
    
    {\\displaystyle {\\mathfrak {I}}(z)}
  
: for example, 
  
    
      
        Re
        ⁡
        (
        2
        +
        3
        i
        )
        =
        2
      
    
    {\\textstyle \\operatorname {Re} (2+3i)=2}
  
, 
  
    
      
        Im
        ⁡
        (
        2
        +
        3
        i
        )
        =
        3
      
    
    {\\displaystyle \\operatorname {Im} (2+3i)=3}
  
.
A complex number z can be identified with the ordered pair of real numbers 
  
    
      
        (
        ℜ
        (
        z
        )
        ,
        ℑ
        (
        z
        )
        )
      
    
    {\\displaystyle (\\Re (z),\\Im (z))}
  
, which may be interpreted as coordinates of a point in a Euclidean plane with standard coordinates, which is then called the complex plane or Argand diagram. The horizontal axis is generally used to display the real part, with increasing values to the right, and the imaginary part marks the vertical axis, with increasing values upwards. 
A real number a can be regarded as a complex number a + 0i, whose imaginary part is 0. A purely imaginary number bi is a complex number 0 + bi, whose real part is zero. It is common to write a + 0i = a, 0 + bi = bi, and a + (−b)i = a − bi; for example, 3 + (−4)i = 3 − 4i.
The set of all complex numbers is denoted by 
  
    
      
        
          C
        
      
    
    {\\displaystyle \\mathbb {C} }
  
 (blackboard bold) or C (upright bold).
In some disciplines such as electromagnetism and electrical engineering, j is used instead of i, as i frequently represents electric current, and complex numbers are written as a + bj or a + jb.


=== Addition and subtraction ===

Two complex numbers 
  
    
      
        a
        =
        x
        +
        y
        i
      
    
    {\\displaystyle a=x+yi}
  
 and 
  
    
      
        b
        =
        u
        +
        v
        i
      
    
    {\\displaystyle b=u+vi}
  
 are added by separately adding their real and imaginary parts.""",
    tier=4,
    domain="quantum",
    source="Wikipedia, 'Complex number'",
    source_url="https://en.wikipedia.org/wiki/Complex_number",
))

register_atom(Atom(
    atom_type="formula",
    name="complex_modulus",
    content="""In algebra, an absolute value is a function that generalizes the usual absolute value. More precisely, if D is a field or (more generally) an integral domain, an absolute value on D is a function, commonly denoted 
  
    
      
        
          |
        
        x
        
          |
        
        ,
      
    
    {\\displaystyle |x|,}
  
 from D to the real numbers  satisfying:

It follows from the axioms that 
  
    
      
        
          |
        
        1
        
          |
        
        =
        1
        ,
      
    
    {\\displaystyle |1|=1,}
  
  
  
    
      
        
          |
        
        −
        1
        
          |
        
        =
        1
        ,
      
    
    {\\displaystyle |-1|=1,}
  
 and 
  
    
      
        
          |
        
        −
        x
        
          |
        
        =
        
          |
        
        x
        
          |
        
      
    
    {\\displaystyle |-x|=|x|}
  
 for every ⁠
  
    
      
        x
      
    
    {\\displaystyle x}
  
⁠. Furthermore, for every positive integer n,

  
    
      
        
          |
        
        n
        
          |
        
        ≤
        n
        ,
      
    
    {\\displaystyle |n|\\leq n,}
  
 where the leftmost n denotes the sum of n summands equal to the identity element of D.
The classical absolute value and its square root are examples of absolute values, but the square of the classical absolute value is not, as it does not fulfill the triangular inequality.
An absolute value induces a metric (and thus a topology) on D by setting 
  
    
      
        d
        (
        x
        ,
        y
        )
        =
        
          |
        
        x
        −
        y
        
          |
        
        .
      
    
    {\\displaystyle d(x,y)=|x-y|.}
  


== Examples ==
The standard absolute value on the integers, the rationals and the real numbers: 
  
    
      
        
          |
        
        x
        
          |
        
        =
        x
      
    
    {\\displaystyle |x|=x}
  
 for 
  
    
      
        x
        ≥
        0
      
    
    {\\displaystyle x\\geq 0}
  
 and 
  
    
      
        
          |
        
        x
        
          |
        
        =
        −
        x
      
    
    {\\displaystyle |x|=-x}
  
 for 
  
    
      
        x
        <
        0
      
    
    {\\displaystyle x<0}
  
.
The standard absolute value or modulus on the complex numbers: 
  
    
      
        
          |
        
        a
        +
        b
        i
        
          |
        
        =
        
          
            
              a
              
                2
              
            
            +
            
              b
              
                2
              
            
          
        
      
    
    {\\displaystyle |a+bi|={\\sqrt {a^{2}+b^{2}}}}
  
 for 
  
    
      
        a
        ,
        b
        ∈
        
          R
        
      
    
    {\\displaystyle a,b\\in \\mathbb {R} }
  
.
The p-adic absolute value on the rational numbers, where p is a fixed prime: 
  
    
      
        
          |
        
        0
        
          
            |
          
          
            p
          
        
        =
        0
      
    
    {\\displaystyle |0|_{p}=0}
  
 and for 
  
    
      
        x
        ≠
        0
      
    
    {\\displaystyle x\\neq 0}
  
 we set 
  
    
      
        
          |
        
        x
        
          
            |
          
          
            p
          
        
        =
        
          p
          
            −
            n
          
        
      
    
    {\\displaystyle |x|_{p}=p^{-n}}
  
, where n is the unique integer such that 
  
    
      
        x
        =
        
          p
          
            n
          
        
        
          
            a
            b
          
        
      
    
    {\\displaystyle x=p^{n}{\\frac {a}{b}}}
  
 and a and b are two integers coprime with p.
The p-adic absolute value on the p-adic numbers, arising from the completion (see § Completions below) of the rationals with the absolute value defined above.
If 
  
    
      
        F
        (
        x
        )
      
    
    {\\displaystyle F(x)}
  
 is the field of rational fractions over a field F in the variable x and 
  
    
      
        P
      
    
    {\\displaystyle P}
  
 is a fixed irreducible polynomial over F, the P-adic absolute value on 
  
    
      
        F
        (
        x
        )
      
    
    {\\displaystyle F(x)}
  
 is defined as follows: 
  
    
      
        
          |
        
        0
        
          
            |
          
          
            P
          
        
        =
        0
      
    
    {\\displaystyle |0|_{P}=0}
  
 and for 
  
    
      
        f
        ≠
        0
      
    
    {\\displaystyle f\\neq 0}
  
 we set 
  
    
      
        
          |
        
        f
        
          
            |
          
          
            P
          
        
        =
        
          2
          
            −
            n
          
        
        ,
      
    
    {\\displaystyle |f|_{P}=2^{-n},}
  
 where n is the unique integer such that 
  
    
      
        f
        =
        
          P
          
            n
          
        
        
          
            G
            H
          
        
        ,
      
    
    {\\textstyle f=P^{n}{\\frac {G}{H}},}
  
 where G and H are two polynomials, both coprime with P.
Absolute values are used to define or characterize global and local fields.


== Types of absolute value ==
The trivial absolute value is the absolute value with |x| = 0 when x = 0 and |x| = 1 otherwise.  Every integral domain can carry at least the trivial absolute value. The trivial value is the only possible absolute value on a finite field because any non-zero element can be raised to some power to yield 1.
If an absolute value satisfies the stronger property |x + y| ≤ max(|x|, |y|) for all x and y, then |x| is called an ultrametric or non-Archimedean absolute value, and otherwise an Archimedean absolute value.


== Places ==
If |x|1 and |x|2 are two absolute values on the same integral domain D, then the two absolute values are equivalent if |x|1 < 1 if and only if |x|2 < 1 for all x. If two nontrivial absolute values are equivalent, then for some exponent e we have |x|1e = |x|2 for all x. Raising an absolute value to a power less than 1 results in another absolute value, but raising to a power greater than 1 does not necessarily result in an absolute value.""",
    tier=4,
    domain="quantum",
    source="Wikipedia, 'Absolute value (algebra)'",
    source_url="https://en.wikipedia.org/wiki/Absolute_value_%28algebra%29",
))

register_atom(Atom(
    atom_type="theorem",
    name="euler_formula",
    content="""Euler's formula, named after Leonhard Euler, is a mathematical formula in complex analysis that establishes the fundamental relationship between the trigonometric functions and the complex exponential function. Euler's formula states that, for any real number x, one has

  
    
      
        
          e
          
            i
            x
          
        
        =
        cos
        ⁡
        x
        +
        i
        sin
        ⁡
        x
        ,
      
    
    {\\displaystyle e^{ix}=\\cos x+i\\sin x,}
  

where e is the base of the natural logarithm, i is the imaginary unit, and cos and sin are the trigonometric functions cosine and sine respectively. This complex exponential function is sometimes denoted cis x ("cosine plus i sine"). The formula is still valid if x is a complex number, and is also called Euler's formula in this more general case.
Euler's formula is ubiquitous in mathematics, physics, chemistry, and engineering. The physicist Richard Feynman called the equation "our jewel" and "the most remarkable formula in mathematics".
When x = π, Euler's formula may be rewritten as eiπ = −1 or eiπ + 1 = 0, which is known as Euler's identity.


== History ==
In 1714, the English mathematician Roger Cotes presented a geometrical argument that can be interpreted (after correcting a misplaced factor of 
  
    
      
        
          
            −
            1
          
        
      
    
    {\\displaystyle {\\sqrt {-1}}}
  
) as:

  
    
      
        i
        x
        =
        ln
        ⁡
        (
        cos
        ⁡
        x
        +
        i
        sin
        ⁡
        x
        )
        .
      
    
    {\\displaystyle ix=\\ln(\\cos x+i\\sin x).}
  

Exponentiating this equation yields Euler's formula. Note that the logarithmic statement is not universally correct for complex numbers, since a complex logarithm can have infinitely many values, differing by multiples of 2πi.

Around 1740, Leonhard Euler turned his attention to the exponential function and derived the equation named after him by comparing the series expansions of the exponential and trigonometric expressions. The formula was first published in 1748 in his foundational work Introductio in analysin infinitorum.
Johann Bernoulli had found that

  
    
      
        
          
            1
            
              1
              +
              
                x
                
                  2
                
              
            
          
        
        =
        
          
            1
            2
          
        
        
          (
          
            
              
                1
                
                  1
                  −
                  i
                  x
                
              
            
            +
            
              
                1
                
                  1
                  +
                  i
                  x
                
              
            
          
          )
        
        .
      
    
    {\\displaystyle {\\frac {1}{1+x^{2}}}={\\frac {1}{2}}\\left({\\frac {1}{1-ix}}+{\\frac {1}{1+ix}}\\right).}
  

And since

  
    
      
        ∫
        
          
            
              d
              x
            
            
              1
              +
              a
              x
            
          
        
        =
        
          
            1
            a
          
        
        ln
        ⁡
        (
        1
        +
        a
        x
        )
        +
        C
        ,
      
    
    {\\displaystyle \\int {\\frac {dx}{1+ax}}={\\frac {1}{a}}\\ln(1+ax)+C,}
  

the above equation tells us something about complex logarithms by relating natural logarithms to imaginary (complex) numbers. Bernoulli, however, did not evaluate the integral.
Bernoulli's correspondence with Euler (who also knew the above equation) shows that Bernoulli did not fully understand complex logarithms. Euler also suggested that complex logarithms can have infinitely many values.
The view of complex numbers as points in the complex plane was described about 50 years later by Caspar Wessel.


== Definitions of complex exponentiation ==

The exponential function ex for real values of x may be defined in a few different equivalent ways (see Characterizations of the exponential function). Several of these methods may be directly extended to give definitions of ez for complex values of z simply by substituting z in place of x and using the complex algebraic operations. In particular, we may use any of the three following definitions, which are equivalent.""",
    tier=5,
    domain="quantum",
    source="Wikipedia, 'Euler's formula'",
    source_url="https://en.wikipedia.org/wiki/Euler%27s_formula",
))

register_atom(Atom(
    atom_type="formula",
    name="qubit_measure",
    content="""In quantum physics, a measurement is the testing or manipulation of a physical system to yield a numerical result. A fundamental feature of quantum theory is that the predictions it makes are probabilistic. 
The procedure for finding a probability involves combining a quantum state, which mathematically describes a quantum system, with a mathematical representation of the measurement to be performed on that system. The formula for this calculation is known as the Born rule. For example, a quantum particle like an electron can be described by a quantum state that associates to each point in space a complex number called a probability amplitude. Applying the Born rule to these amplitudes gives the probabilities that the electron will be found in one region or another when an experiment is performed to locate it. This is the best the theory can do; it cannot say for certain where the electron will be found. The same quantum state can also be used to make a prediction of how the electron will be moving, if an experiment is performed to measure its momentum instead of its position. The uncertainty principle implies that, whatever the quantum state, the range of predictions for the electron's position and the range of predictions for its momentum cannot both be narrow. Some quantum states imply a near-certain prediction of the result of a position measurement, but the result of a momentum measurement will be highly unpredictable, and vice versa. Furthermore, the fact that nature violates the statistical conditions known as Bell inequalities indicates that the unpredictability of quantum measurement results cannot be explained away as due to ignorance about local hidden variables within quantum systems.
Measuring a quantum system generally changes the quantum state that describes that system. This is a central feature of quantum mechanics, one that is both mathematically intricate and conceptually subtle. The mathematical tools for making predictions about what measurement outcomes may occur, and how quantum states can change, were developed during the 20th century and make use of linear algebra and functional analysis. Quantum physics has proven to be an empirical success and to have wide-ranging applicability. 
On a more philosophical level, debates continue about the meaning of the measurement concept. The different interpretations of quantum mechanics, concern of solving what is known as the measurement problem.


== Mathematical formalism ==


=== "Observables" as self-adjoint operators ===

In quantum mechanics, each physical system is associated with a Hilbert space, each element of which represents a possible state of the physical system. The approach codified by John von Neumann represents a measurement upon a physical system by a self-adjoint operator on that Hilbert space termed an "observable". These observables play the role of measurable quantities familiar from classical physics: position, momentum, energy, angular momentum and so on. The dimension of the Hilbert space may be infinite, as it is for the space of square-integrable functions on a line, which is used to define the quantum physics of a continuous degree of freedom. Alternatively, the Hilbert space may be finite-dimensional, as occurs for spin degrees of freedom. Many treatments of the theory focus on the finite-dimensional case, as the mathematics involved is somewhat less demanding. Indeed, introductory physics texts on quantum mechanics often gloss over mathematical technicalities that arise for continuous-valued observables and infinite-dimensional Hilbert spaces, such as the distinction between bounded and unbounded operators; questions of convergence (whether the limit of a sequence of Hilbert-space elements also belongs to the Hilbert space), exotic possibilities for sets of eigenvalues, like Cantor sets; and so forth. These issues can be satisfactorily resolved using spectral theory; the present article will avoid them whenever possible.


=== Projective measurement ===

The eigenvectors of a von Neumann observable form an orthonormal basis for the Hilbert space, and each possible outcome of that measurement corresponds to one of the vectors comprising the basis. A density operator is a positive-semidefinite operator on the Hilbert space whose trace is equal to 1. For each measurement that can be defined, the probability distribution over the outcomes of that measurement can be computed from the density operator. The procedure for doing so is the Born rule, which states that

  
    
      
        P
        (
        
          x
          
            i
          
        
        )
        =
        tr
        ⁡
        (
        
          Π
          
            i
          
        
        ρ
        )
        ,
      
    
    {\\displaystyle P(x_{i})=\\operatorname {tr} (\\Pi _{i}\\rho ),}
  

where 
  
    
      
        ρ
      
    
    {\\displaystyle \\rho }
  
 is the density operator, and 
  
    
      
        
          Π
          
            i
          
        
      
    
    {\\displaystyle \\Pi _{i}}
  
 is the projection operator onto the basis vector corresponding to the measurement outcome 
  
    
      
        
          x
          
            i
          
        
      
    
    {\\displaystyle x_{i}}
  
. The average of the eigenvalues of a von Neumann observable, weighted by the Born rule probabilities, is the expectation value of that observable. For an observable 
  
    
      
        A
      
    
    {\\displaystyle A}
  
, the expectation value given a quantum state 
  
    
      
        ρ
      
    
    {\\displaystyle \\rho }
  
 is

  
    
      
        ⟨
        A
        ⟩
        =
        tr
        ⁡
        (
        A
        ρ
        )
        .
      
    
    {\\displaystyle \\langle A\\rangle =\\operatorname {tr} (A\\rho ).}
  

A density operator that is a rank-1 projection is known as a pure quantum state, and all quantum states that are not pure are designated mixed. Pure states are also known as wavefunctions. Assigning a pure state to a quantum system implies certainty about the outcome of some measurement on that system (i.e., 
  
    
      
        P
        (
        x
        )
        =
        1
      
    
    {\\displaystyle P(x)=1}
  
 for some outcome 
  
    
      
        x
      
    
    {\\displaystyle x}
  
). Any mixed state can be written as a convex combination of pure states, though not in a unique way. The state space of a quantum system is the set of all states, pure and mixed, that can be assigned to it.
The Born rule associates a probability with each unit vector in the Hilbert space, in such a way that these probabilities sum to 1 for any set of unit vectors comprising an orthonormal basis. Moreover, the probability associated with a unit vector is a function of the density operator and the unit vector, and not of additional information like a choice of basis for that vector to be embedded in. Gleason's theorem establishes the converse: all assignments of probabilities to unit vectors (or, equivalently, to the operators that project onto them) that satisfy these conditions take the form of applying the Born rule to some density operator.


=== Generalized measurement (POVM) ===

In functional analysis and quantum measurement theory, a positive-operator-valued measure (POVM) is a measure whose values are positive semi-definite operators on a Hilbert space. POVMs are a generalisation of projection-valued measures (PVMs) and, correspondingly, quantum measurements described by POVMs are a generalisation of quantum measurement described by PVMs. In rough analogy, a POVM is to a PVM what a mixed state is to a pure state. Mixed states are needed to specify the state of a subsystem of a larger system (see Schrödinger–HJW theorem); analogously, POVMs are necessary to describe the effect on a subsystem of a projective measurement performed on a larger system.""",
    tier=5,
    domain="quantum",
    source="Wikipedia, 'Measurement in quantum mechanics'",
    source_url="https://en.wikipedia.org/wiki/Measurement_in_quantum_mechanics",
))

register_atom(Atom(
    atom_type="formula",
    name="quantum_gate",
    content="""In quantum computing and specifically the quantum circuit model of computation, a quantum logic gate (or simply quantum gate) is a basic quantum circuit operating on a small number of qubits. Quantum logic gates are the building blocks of quantum circuits, like classical logic gates are for conventional digital circuits.
Unlike many classical logic gates, quantum logic gates are reversible. It is possible to perform classical computing using only reversible gates. For example, the reversible Toffoli gate can implement all Boolean functions, often at the cost of having to use ancilla bits. The Toffoli gate has a direct quantum equivalent, showing that quantum circuits can perform all operations performed by classical circuits.
Quantum gates are unitary operators, and are described as unitary matrices relative to some orthonormal basis. Usually the computational basis is used, which unless comparing it with something, just means that for a d-level quantum system (such as a qubit, a quantum register, or qutrits and qudits) the orthonormal basis vectors are labeled 
  
    
      
        
          |
        
        0
        ⟩
        ,
        
          |
        
        1
        ⟩
        ,
        …
        ,
        
          |
        
        d
        −
        1
        ⟩
      
    
    {\\displaystyle |0\\rangle ,|1\\rangle ,\\dots ,|d-1\\rangle }
  
, or use binary notation.


== History ==
The current notation for quantum gates was developed by many of the founders of quantum information science including Adriano Barenco, Charles Bennett, Richard Cleve, David P. DiVincenzo, Norman Margolus, Peter Shor, Tycho Sleator, John A. Smolin, and Harald Weinfurter, building on notation introduced by Richard Feynman in 1986.


== Representation ==

Quantum logic gates are represented by unitary matrices. A gate that acts on 
  
    
      
        n
      
    
    {\\displaystyle n}
  
 qubits (a register) is represented by a 
  
    
      
        
          2
          
            n
          
        
        ×
        
          2
          
            n
          
        
      
    
    {\\displaystyle 2^{n}\\times 2^{n}}
  
 unitary matrix, and the set of all such gates with the group operation of matrix multiplication is the unitary group U(2n). The quantum states that the gates act upon are unit vectors in 
  
    
      
        
          2
          
            n
          
        
      
    
    {\\displaystyle 2^{n}}
  
 complex dimensions, with the complex Euclidean norm (the 2-norm). The basis vectors (sometimes called eigenstates) are the possible outcomes if the state of the qubits is measured, and a quantum state is a linear combination of these outcomes. The most common quantum gates operate on vector spaces of one or two qubits, just like the common classical logic gates operate on one or two bits.
Even though the quantum logic gates belong to continuous symmetry groups, real hardware is inexact and thus limited in precision. The application of gates typically introduces errors, and the quantum states' fidelities decrease over time. If error correction is used, the usable gates are further restricted to a finite set. Later in this article, this is ignored as the focus is on the ideal quantum gates' properties.
Quantum states are typically represented by "kets", from a notation known as bra–ket.
The vector representation of a single qubit is

  
    
      
        
          |
        
        a
        ⟩
        =
        
          v
          
            0
          
        
        
          |
        
        0
        ⟩
        +
        
          v
          
            1
          
        
        
          |
        
        1
        ⟩
        →
        
          
            [
            
              
                
                  
                    v
                    
                      0
                    
                  
                
              
              
                
                  
                    v
                    
                      1
                    
                  
                
              
            
            ]
          
        
        .
      
    
    {\\displaystyle |a\\rangle =v_{0}|0\\rangle +v_{1}|1\\rangle \\rightarrow {\\begin{bmatrix}v_{0}\\\\v_{1}\\end{bmatrix}}.}
  

Here, 
  
    
      
        
          v
          
            0
          
        
      
    
    {\\displaystyle v_{0}}
  
 and 
  
    
      
        
          v
          
            1
          
        
      
    
    {\\displaystyle v_{1}}
  
 are the complex probability amplitudes of the qubit. These values determine the probability of measuring a 0 or a 1, when measuring the state of the qubit. See measurement below for details.
The value zero is represented by the ket 
  
    
      
        
          |
        
        0
        ⟩
        =
        
          
            [
            
              
                
                  1
                
              
              
                
                  0
                
              
            
            ]
          
        
      
    
    {\\displaystyle |0\\rangle ={\\begin{bmatrix}1\\\\0\\end{bmatrix}}}
  
, and the value one is represented by the ket 
  
    
      
        
          |
        
        1
        ⟩
        =
        
          
            [
            
              
                
                  0
                
              
              
                
                  1
                
              
            
            ]
          
        
      
    
    {\\displaystyle |1\\rangle ={\\begin{bmatrix}0\\\\1\\end{bmatrix}}}
  
.
The tensor product (or Kronecker product) is used to combine quantum states. The combined state for a qubit register is the tensor product of the constituent qubits.""",
    tier=6,
    domain="quantum",
    source="Wikipedia, 'Quantum logic gate'",
    source_url="https://en.wikipedia.org/wiki/Quantum_logic_gate",
))

register_atom(Atom(
    atom_type="theorem",
    name="boolean_algebra",
    content="""In mathematics and mathematical logic, Boolean algebra is a branch of algebra. It differs from elementary algebra in two ways. First, the values of the variables are the truth values true and false, usually denoted by 1 and 0, whereas in elementary algebra the values of the variables are numbers. Second, Boolean algebra uses logical operators such as conjunction (and) denoted as ∧, disjunction (or) denoted as ∨, and negation (not) denoted as ¬. Elementary algebra, on the other hand, uses arithmetic operators such as addition, multiplication, subtraction, and division. Boolean algebra is therefore a formal way of describing logical operations in the same way that elementary algebra describes numerical operations.
Boolean algebra was introduced by George Boole in his first book The Mathematical Analysis of Logic (1847), and set forth more fully in his An Investigation of the Laws of Thought (1854). According to Huntington, the term Boolean algebra was first suggested by Henry M. Sheffer in 1913, although Charles Sanders Peirce gave the title "A Boolian [sic] Algebra with One Constant" to the first chapter of his "The Simplest Mathematics" in 1880. Boolean algebra has been fundamental in the development of digital electronics, and is provided for in all modern programming languages. It is also used in set theory and statistics.


== History ==
A precursor of Boolean algebra was Gottfried Wilhelm Leibniz's algebra of concepts. The usage of binary in relation to the I Ching was central to Leibniz's characteristica universalis. It eventually created the foundations of algebra of concepts. Leibniz's algebra of concepts is deductively equivalent to the Boolean algebra of sets.
Boole's algebra predated the modern developments in abstract algebra and mathematical logic; it is however seen as connected to the origins of both fields. In an abstract setting, Boolean algebra was perfected in the late 19th century by Jevons, Schröder, Huntington and others, until it reached the modern conception of an (abstract) mathematical structure. For example, the empirical observation that one can manipulate expressions in the algebra of sets, by translating them into expressions in Boole's algebra, is explained in modern terms by saying that the algebra of sets is a Boolean algebra (note the indefinite article). In fact, M. H. Stone proved in 1936 that every Boolean algebra is isomorphic to a field of sets.
In the 1930s, while studying switching circuits, Claude Shannon observed that one could also apply the rules of Boole's algebra in this setting, and he introduced switching algebra as a way to analyze and design circuits by algebraic means in terms of logic gates. Shannon already had at his disposal the abstract mathematical apparatus, thus he cast his switching algebra as the two-element Boolean algebra. In modern circuit engineering settings, there is little need to consider other Boolean algebras, thus "switching algebra" and "Boolean algebra" are often used interchangeably.
Efficient implementation of Boolean functions is a fundamental problem in the design of combinational logic circuits. Modern electronic design automation tools for very-large-scale integration (VLSI) circuits often rely on an efficient representation of Boolean functions known as (reduced ordered) binary decision diagrams (BDD) for logic synthesis and formal verification.
Logic sentences that can be expressed in classical propositional calculus have an equivalent expression in Boolean algebra. Thus, Boolean logic is sometimes used to denote propositional calculus performed in this way. Boolean algebra is not sufficient to capture logic formulas using quantifiers, like those from first-order logic.
Although the development of mathematical logic did not follow Boole's program, the connection between his algebra and logic was later put on firm ground in the setting of algebraic logic, which also studies the algebraic systems of many other logics. The problem of determining whether the variables of a given Boolean (propositional) formula can be assigned in such a way as to make the formula evaluate to true is called the Boolean satisfiability problem (SAT), and is of importance to theoretical computer science, being the first problem shown to be NP-complete. The closely related model of computation known as a Boolean circuit relates time complexity (of an algorithm) to circuit complexity.


== Values ==
Whereas expressions denote mainly numbers in elementary algebra, in Boolean algebra, they denote the truth values false and true. These values are represented with the bits, 0 and 1. They do not behave like the integers 0 and 1, for which 1 + 1 = 2, but may be identified with the elements of the two-element field GF(2), that is, integer arithmetic modulo 2, for which 1 + 1 = 0. Addition and multiplication then play the Boolean roles of XOR (exclusive-or) and AND (conjunction), respectively, with disjunction x ∨ y (inclusive-or) definable as x + y − xy and negation ¬x as 1 − x. In GF(2), − may be replaced by +, since they denote the same operation; however, this way of writing Boolean operations allows applying the usual arithmetic operations of integers (this may be useful when using a programming language in which GF(2) is not implemented).
Boolean algebra also deals with functions which have their values in the set {0,1}. A sequence of bits is a commonly used example of such a function. Another common example is the totality of subsets of a set E: to a subset F of E, one can define the indicator function that takes the value 1 on F, and 0 outside F. The most general example is the set elements of a Boolean algebra, with all of the foregoing being instances thereof.
As with elementary algebra, the purely equational part of the theory may be developed, without considering explicit values for the variables.


== Operations ==


=== Basic operations ===
While elementary algebra has four operations (addition, subtraction, multiplication, and division), the Boolean algebra has only three basic operations: conjunction, disjunction, and negation, expressed with the corresponding binary operators AND (
  
    
      
        ∧
      
    
    {\\displaystyle \\land }
  
) and OR (
  
    
      
        ∨
      
    
    {\\displaystyle \\lor }
  
) and the unary operator NOT (
  
    
      
        ¬
      
    
    {\\displaystyle \\neg }
  
), collectively referred to as Boolean operators. Variables in Boolean algebra that store the logical value of 0 and 1 are called the Boolean variables. They are used to store either true or false values. The basic operations on Boolean variables x and y are defined as follows:
Alternatively, the values of x ∧ y, x ∨ y, and ¬x can be expressed by tabulating their values with truth tables as follows:

When used in expressions, the operators are applied according to the precedence rules.""",
    tier=3,
    domain="computer_science",
    source="Wikipedia, 'Boolean algebra'",
    source_url="https://en.wikipedia.org/wiki/Boolean_algebra",
))

register_atom(Atom(
    atom_type="algorithm",
    name="binary_arithmetic",
    content="""A binary number is a number expressed in the base-2 numeral system or binary numeral system, a method for representing numbers that uses only two symbols for the natural numbers: typically 0 (zero) and 1 (one). A binary number may also refer to a rational number that has a finite representation in the binary numeral system, that is, the quotient of an integer by a power of two.
The base-2 numeral system is a positional notation with a radix of 2. Each digit is referred to as a bit, or binary digit. Because of its straightforward implementation in digital electronic circuitry using logic gates, the binary system is used by almost all modern computers and computer-based devices, as a preferred system of use, over various other human techniques of communication, because of the simplicity of the language and the noise immunity in physical implementation.


== History ==
The modern binary number system was first studied in Europe in the 16th and 17th centuries by Thomas Harriot, and decades later by Gottfried Leibniz, who is credited for the invention. However, systems related to binary numbers have appeared earlier in multiple cultures including ancient Egypt, China, Europe and India, e.g. in relation to divination using binary lots. 


=== Egypt ===

The scribes of ancient Egypt used two different systems for their fractions, Egyptian fractions (not related to the binary number system) and Horus-Eye fractions (so called because some historians of mathematics believed that the symbols used for this system could be arranged to form the eye of Horus, although this has been disputed). Horus-Eye fractions are a binary numbering system for fractional quantities of grain, liquids, or other measures, in which a fraction of a hekat is expressed as a sum of the binary fractions 1⁄2, 1⁄4, 1⁄8, 1⁄16, 1⁄32, and 1⁄64. Early forms of this system can be found in documents from the Fifth Dynasty of Egypt, approximately 2400 BC, and its fully developed hieroglyphic form dates to the Nineteenth Dynasty of Egypt, approximately 1200 BC.
The method used for ancient Egyptian multiplication is also closely related to binary numbers. In this method, multiplying one number by a second is performed by a sequence of steps in which a value (initially the first of the two numbers) is either doubled or has the first number added back into it; the order in which these steps are to be performed is given by the binary representation of the second number. This method can be seen in use, for instance, in the Rhind Mathematical Papyrus, which dates to around 1650 BC.


=== China ===

The I Ching dates from the 9th century BC in China. The binary notation in the I Ching is used to interpret its quaternary technique of divination.
It is based on taoistic duality of yin and yang. Eight trigrams (Bagua) and a set of 64 hexagrams ("sixty-four" gua), analogous to the three-bit and six-bit binary numerals, were in use at least as early as the Zhou dynasty of ancient China.
The Song dynasty scholar Shao Yong (1011–1077) rearranged the hexagrams in a format that resembles modern binary numbers, although he did not intend his arrangement to be used mathematically. Viewing the least significant bit on top of single hexagrams in Shao Yong's square
and reading along rows either from bottom right to top left with solid lines as 0 and broken lines as 1 or from top left to bottom right with solid lines as 1 and broken lines as 0 hexagrams can be interpreted as sequence from 0 to 63.


=== Classical antiquity ===
Etruscans divided the outer edge of divination livers into sixteen parts, each inscribed with the name of a divinity and its region of the sky. Each liver region produced a binary reading which was combined into a final binary for divination. 
Divination at Ancient Greek Dodona oracle worked by drawing from separate jars, questions tablets and "yes" and "no" pellets. The result was then combined to make a final prophecy.


=== India ===
The Indian scholar Pingala (c. 2nd century BC) developed a binary system for describing prosody. He described meters in the form of short and long syllables (the latter equal in length to two short syllables). They were known as laghu (light) and guru (heavy) syllables.
Pingala's Hindu classic titled Chandaḥśāstra (8.23) describes the formation of a matrix in order to give a unique value to each meter. "Chandaḥśāstra" literally translates to science of meters in Sanskrit. The binary representations in Pingala's system increases towards the right, and not to the left like in the binary numbers of the modern positional notation. In Pingala's system, the numbers start from number one, and not zero. Four short syllables "0000" is the first pattern and corresponds to the value one. The numerical value is obtained by adding one to the sum of place values.


=== West Africa ===
The Ifá is a West African divination system popular among the Yoruba tribe of the Old Oyo Empire. Similar to the I Ching, but has up to 256 binary signs, unlike the I Ching which has 64. The number comes from squaring 16 which also matches the total possibilities in an 8-bit sequence. In Ifá divination, this reflects the possible outcomes called Odú. These Odú are determined using an Ọpẹlẹ chain, which has 8 seeds. Each seed can land in one of two positions (open or closed) creating all the possible combinations. The Ifá originated in 15th century West Africa among Yoruba people. In 2008, UNESCO added Ifá to its list of the "Masterpieces of the Oral and Intangible Heritage of Humanity".


=== Other cultures ===
The residents of the island of Mangareva in French Polynesia were using a hybrid binary-decimal system before 1450. Slit drums with binary tones are used to encode messages across Africa and Asia.
Sets of binary combinations similar to the I Ching have also been used in traditional African divination systems, such as Ifá among others, as well as in medieval Western geomancy. The majority of Indigenous Australian languages use a base-2 system.


=== Western predecessors to Leibniz ===
In the late 13th century Ramon Llull had the ambition to account for all wisdom in every branch of human knowledge of the time. For that purpose he developed a general method or "Ars generalis" based on binary combinations of a number of simple basic principles or categories, for which he has been considered a predecessor of computing science and artificial intelligence.
In 1605, Francis Bacon discussed a system whereby letters of the alphabet could be reduced to sequences of binary digits, which could then be encoded as scarcely visible variations in the font in any random text. Importantly for the general theory of binary encoding, he added that this method could be used with any objects at all: "provided those objects be capable of a twofold difference only; as by Bells, by Trumpets, by Lights and Torches, by the report of Muskets, and any instruments of like nature".

In 1617, John Napier described a system he called location arithmetic for doing binary calculations using a non-positional representation by letters.
Thomas Harriot investigated several positional numbering systems, including binary, but did not publish his results; they were found later among his papers.
Possibly the first publication of the system in Europe was by Juan Caramuel y Lobkowitz, in 1700.


=== Leibniz ===

Leibniz wrote in excess of a hundred manuscripts on binary, most of them remaining unpublished. Before his first dedicated work in 1679, numerous manuscripts feature early attempts to explore binary concepts, including tables of numbers and basic calculations, often scribbled in the margins of works unrelated to mathematics.
His first known work on binary, “On the Binary Progression", in 1679, Leibniz introduced conversion between decimal and binary, along with algorithms for performing basic arithmetic operations such as addition, subtraction, multiplication, and division using binary numbers.""",
    tier=3,
    domain="computer_science",
    source="Wikipedia, 'Binary number'",
    source_url="https://en.wikipedia.org/wiki/Binary_number",
))

register_atom(Atom(
    atom_type="algorithm",
    name="twos_complement",
    content="""Two's complement is the most common method of representing signed (positive, negative, and zero) integers on computers, and more generally, fixed point binary values. As with the ones' complement and sign-magnitude systems, two's complement uses the most significant bit as the sign to indicate positive (0) or negative (1) numbers, and nonnegative numbers are given their unsigned representation (6 is 0110, zero is 0000); however, in two's complement, negative numbers are represented by taking the bit complement of their magnitude and then adding one (−6 is 1010). The number of bits in the representation may be increased by padding all additional high bits of negative or positive numbers with 1's or 0's, respectively, or decreased by removing additional leading 1's or 0's.
Unlike the ones' complement scheme, the two's complement scheme has only one representation for zero, with room for one extra negative number (the range of a 4-bit number is −8 to +7). Furthermore, the same arithmetic implementations can be used on signed as well as unsigned integers
and differ only in the integer overflow situations, since the sum of representations of a positive number and its negative is 0 (with the carry bit set).


== Procedure ==
The following is the procedure for obtaining the two's complement representation of a given negative number in binary digits:

Step 1: starting with the absolute binary representation of the number, with the leading bit being a sign bit;
Step 2: inverting (or flipping) all bits – changing every 0 to 1, and every 1 to 0;
Step 3: adding 1 to the entire inverted number, ignoring any overflow. Accounting for overflow will produce the wrong value for the result.
For example, to calculate the decimal number −6 in binary from the number 6:

Step 1: +6 in decimal is 0110 in binary; the leftmost significant bit (the first 0) is the sign (just 110 in binary would be −2 in decimal).
Step 2: flip all bits in 0110, giving 1001.
Step 3: add the place value 1 to the flipped number 1001, giving 1010.
To verify that 1010 indeed has a value of −6, add the place values together, but subtract the sign value from the final calculation. Because the most significant value is the sign value, it must be subtracted to produce the correct result: 1010 = −(1×23) + (0×22) + (1×21) + (0×20) = 1×−8 + 0 + 1×2 + 0 = −6. 

Steps 2 and 3 together are a valid method to compute the additive inverse 
  
    
      
        −
        n
      
    
    {\\displaystyle -n}
  
 of any (positive or negative) integer 
  
    
      
        n
      
    
    {\\displaystyle n}
  
 where both input and output are in two's complement. An alternative to compute 
  
    
      
        −
        n
      
    
    {\\displaystyle -n}
  
 is to use subtraction 
  
    
      
        0
        −
        n
      
    
    {\\displaystyle 0-n}
  
. See below for subtraction of integers in two's complement.


== Theory ==

Two's complement is an example of a radix complement. The 'two' in the name refers to the number 2N - "two to the power of N", which is the value in respect to which the complement is calculated in an N-bit system (the only case where exactly 'two' would be produced in this term is N = 1, so for a 1-bit system, but these do not have capacity for both a sign and a zero). As such, the precise definition of the two's complement of an N-bit number is the complement of that number with respect to 2N.
The defining property of being a complement to a number with respect to 2N is simply that the summation of this number with the original produce 2N. For example, using binary with numbers up to three bits (so N = 3 and 2N = 23 = 8 = 10002, where '2' indicates a binary representation), a two's complement for the number 3 (0112) is 5 (1012), because summed to the original it gives 23 = 10002 = 0112 + 1012. Where this correspondence is employed for representing negative numbers, it effectively means, using an analogy with decimal digits and a number-space only allowing eight non-negative numbers 0 through 7, dividing the number-space into two sets: the first four of the numbers 0 1 2 3 remain the same, while the remaining four encode negative numbers, maintaining their growing order, so making 4 encode −4, 5 encode −3, 6 encode −2 and 7 encode −1. A binary representation has an additional utility however, because the most significant bit also indicates the group (and the sign): it is 0 for the first group of non-negatives, and 1 for the second group of negatives. The tables at right illustrate this property.

Calculation of the binary two's complement of a positive number essentially means subtracting the number from the 2N. But as can be seen for the three-bit example and the four-bit 10002 (23), the number 2N will not itself be representable in a system limited to N bits, as it is just outside the N bits space (the number is nevertheless the reference point of the "Two's complement" in an N-bit system). Because of this, systems with maximally N-bits must break the subtraction into two operations: first subtract from the maximum number in the N-bit system, that is 2N−1 (this term in binary is actually a simple number consisting of 'all 1s', and a subtraction from it can be done simply by inverting all bits in the number also known as the bitwise NOT operation) and then adding the one. Coincidentally, that intermediate number before adding the one is also used in computer science as another method of signed number representation and is called a ones' complement (named that because summing such a number with the original gives the 'all 1s').
Compared to other systems for representing signed numbers (e.g., ones' complement), the two's complement has the advantage that the fundamental arithmetic operations of addition, subtraction, and multiplication are identical to those for unsigned binary numbers (as long as the inputs are represented in the same number of bits as the output, and any overflow beyond those bits is discarded from the result). This property makes the system simpler to implement, especially for higher-precision arithmetic. Additionally, unlike ones' complement systems, two's complement has no representation for negative zero, and thus does not suffer from its associated difficulties. Otherwise, both schemes have the desired property that the sign of integers can be reversed by taking the complement of its binary representation, but two's complement has an exception – the lowest negative, as can be seen in the tables.


== History ==
The method of complements had long been used to perform subtraction in decimal adding machines and mechanical calculators. John von Neumann suggested use of two's complement binary representation in his 1945 First Draft of a Report on the EDVAC proposal for an electronic stored-program digital computer. The 1949 EDSAC, which was inspired by the First Draft, used two's complement representation of negative binary integers.
Many early computers, including the CDC 6600, the LINC, the PDP-1, and the UNIVAC 1107, use ones' complement notation; the descendants of the UNIVAC 1107, the UNIVAC 1100/2200 series, continued to do so.  (Later 18-bit DEC machines supported both ones'-complement addition with the ADD instruction and two's-complement arithmetic with the TAD instruction.) The IBM 700/7000 series scientific machines use sign/magnitude notation, except for the index registers which are two's complement. Early commercial computers storing negative values in two's complement form include the English Electric DEUCE (1955) and the Digital Equipment Corporation PDP-5 (1963) and PDP-6 (1964).""",
    tier=4,
    domain="computer_science",
    source="Wikipedia, 'Two's complement'",
    source_url="https://en.wikipedia.org/wiki/Two%27s_complement",
))

register_atom(Atom(
    atom_type="definition",
    name="logic_gate_eval",
    content="""A logic gate is a device that performs a Boolean function, a logical operation performed on one or more binary inputs that produces a single binary output. Depending on the context, the term may refer to an ideal logic gate, one that has, for instance, zero rise time and unlimited fan-out, or it may refer to a non-ideal physical device (see ideal and real op-amps for comparison).
The primary way of building logic gates uses diodes or transistors acting as electronic switches. Today, most logic gates are made from MOSFETs (metal–oxide–semiconductor field-effect transistors). They can also be constructed using vacuum tubes, electromagnetic relays with relay logic, fluidic logic, pneumatic logic, optics, molecules, acoustics, or even mechanical or thermal elements.
Logic gates can be cascaded in the same way that Boolean functions can be composed, allowing the construction of a physical model of all of Boolean logic, and therefore, all of the algorithms and mathematics that can be described with Boolean logic. Logic circuits include such devices as multiplexers, registers, arithmetic logic units (ALUs), and computer memory, all the way up through complete microprocessors, which may contain more than 100 million logic gates.
Compound logic gates AND-OR-invert (AOI) and OR-AND-invert (OAI) are often employed in circuit design because their construction using MOSFETs is simpler and more efficient than the sum of the individual gates.
There are seven basic logic gates: NOT, OR, NOR (Negation of the OR statement), AND, NAND (Negation of the AND statement), XOR (Exclusive OR), XNOR (Negation of the Exclusive OR statement).


== History and development ==
The binary number system was refined by Gottfried Wilhelm Leibniz (published in 1705), influenced by the ancient I Ching's binary system. Leibniz established that using the binary system combined the principles of arithmetic and logic.
The analytical engine devised by Charles Babbage in 1837 used mechanical logic gates based on gears.
In an 1886 letter, Charles Sanders Peirce described how logical operations could be carried out by electrical switching circuits. Early Electromechanical computers were constructed from switches and relay logic rather than the later innovations of vacuum tubes (thermionic valves) or transistors (from which later electronic computers were constructed). Ludwig Wittgenstein introduced a version of the 16-row truth table as proposition 5.101 of Tractatus Logico-Philosophicus (1921). Walther Bothe, inventor of the coincidence circuit, got part of the 1954 Nobel Prize in physics, for the first modern electronic AND gate in 1924. Konrad Zuse designed and built electromechanical logic gates for his computer Z1 (from 1935 to 1938).
From 1934 to 1936, NEC engineer Akira Nakashima, Claude Shannon and Victor Shestakov introduced switching circuit theory in a series of papers showing that two-valued Boolean algebra, which they discovered independently, can describe the operation of switching circuits. Using this property of electrical switches to implement logic is the fundamental concept that underlies all electronic digital computers. Switching circuit theory became the foundation of digital circuit design, as it became widely known in the electrical engineering community during and after World War II, with theoretical rigor superseding the ad hoc methods that had prevailed previously.
In 1948, Bardeen and Brattain patented an insulated-gate transistor (IGFET) with an inversion layer. Their concept forms the basis of CMOS technology today. In 1957, Frosch and Derick were able to manufacture PMOS and NMOS planar gates. Later a team at Bell Labs demonstrated a working MOS with PMOS and NMOS gates. Both types were later combined and adapted into complementary MOS (CMOS) logic by Chih-Tang Sah and Frank Wanlass at Fairchild Semiconductor in 1963.


== Symbols ==

There are two sets of symbols for elementary logic gates in common use, both defined in ANSI/IEEE Std 91-1984 and its supplement ANSI/IEEE Std 91a-1991. The "distinctive shape" set, based on traditional schematics, is used for simple drawings and derives from United States Military Standard MIL-STD-806 of the 1950s and 1960s. It is sometimes unofficially described as "military", reflecting its origin. The "rectangular shape" set, based on ANSI Y32.14 and other early industry standards as later refined by IEEE and IEC, has rectangular outlines for all types of gate and allows representation of a much wider range of devices than is possible with the traditional symbols. The IEC standard, IEC 60617-12, has been adopted by other standards, such as EN 60617-12:1999 in Europe, BS EN 60617-12:1999 in the United Kingdom, and DIN EN 60617-12:1998 in Germany.
The mutual goal of IEEE Std 91-1984 and IEC 617-12 was to provide a uniform method of describing the complex logic functions of digital circuits with schematic symbols. These functions were more complex than simple AND and OR gates. They could be medium-scale circuits such as a 4-bit counter to a large-scale circuit such as a microprocessor.
IEC 617-12 and its renumbered successor IEC 60617-12 do not explicitly show the "distinctive shape" symbols, but do not prohibit them. These are, however, shown in ANSI/IEEE Std 91 (and 91a) with this note: "The distinctive-shape symbol is, according to IEC Publication 617, Part 12, not preferred, but is not considered to be in contradiction to that standard." IEC 60617-12 correspondingly contains the note (Section 2.1) "Although non-preferred, the use of other symbols recognized by official national standards, that is distinctive shapes in place of symbols [list of basic gates], shall not be considered to be in contradiction with this standard. Usage of these other symbols in combination to form complex symbols (for example, use as embedded symbols) is discouraged." This compromise was reached between the respective IEEE and IEC working groups to permit the IEEE and IEC standards to be in mutual compliance with one another.
In the 1980s, schematics were the predominant method to design both circuit boards and custom ICs known as gate arrays. Today custom ICs and the field-programmable gate array are typically designed with Hardware Description Languages (HDL) such as Verilog or VHDL.


== De Morgan equivalent symbols ==
By use of De Morgan's laws, an AND function is identical to an OR function with negated inputs and outputs. Likewise, an OR function is identical to an AND function with negated inputs and outputs. A NAND gate is equivalent to an OR gate with negated inputs, and a NOR gate is equivalent to an AND gate with negated inputs.
This leads to an alternative set of symbols for basic gates that use the opposite core symbol (AND or OR) but with the inputs and outputs negated. Use of these alternative symbols can make logic circuit diagrams much clearer and help to show accidental connection of an active high output to an active low input or vice versa. Any connection that has logic negations at both ends can be replaced by a negationless connection and a suitable change of gate or vice versa. Any connection that has a negation at one end and no negation at the other can be made easier to interpret by instead using the De Morgan equivalent symbol at either of the two ends. When negation or polarity indicators on both ends of a connection match, there is no logic negation in that path (effectively, bubbles "cancel"), making it easier to follow logic states from one symbol to the next. This is commonly seen in real logic diagrams – thus the reader must not get into the habit of associating the shapes exclusively as OR or AND shapes, but also take into account the bubbles at both inputs and outputs in order to determine the "true" logic function indicated.
A De Morgan symbol can show more clearly a gate's primary logical purpose and the polarity of its nodes that are considered in the "signaled" (active, on) state.""",
    tier=3,
    domain="computer_science",
    source="Wikipedia, 'Logic gate'",
    source_url="https://en.wikipedia.org/wiki/Logic_gate",
))

register_atom(Atom(
    atom_type="formula",
    name="sigmoid_eval",
    content="""A sigmoid function is any mathematical function whose graph has a characteristic S-shaped or sigmoid curve.
A common example of a sigmoid function is the logistic function.
Other sigmoid functions are given in the Examples section. In some fields, most notably in the context of artificial neural networks, the term "sigmoid function" is used as a synonym for "logistic function".
Special cases of sigmoid functions include the Gompertz curve (used in modeling systems that saturate at large values of x) and the ogee curve (used in the spillway of some dams). Sigmoid functions have domain of all real numbers, with return (response) value commonly monotonically increasing but could be decreasing. Sigmoid functions most often show a return value (y axis) in the range 0 to 1. Another commonly used range is from −1 to 1.
There is also the Heaviside step function, which instantaneously transitions between 0 and 1.
A wide variety of sigmoid functions including the logistic and hyperbolic tangent functions have been used as the activation function of artificial neurons. Sigmoid curves are also common in statistics as cumulative distribution functions (which go from 0 to 1), such as the integrals of the logistic density, the normal density, and Student's t probability density functions. The logistic sigmoid function is invertible, and its inverse is the logit function.


== Theory ==
In mathematics, a unitary sigmoid function is a bounded sigmoid-type function normalized to the unit range, typically with lower and upper asymptotes at 0 and 1. The theory proposed by Grebenc distinguishes three kinds of unitary sigmoid functions according to their asymptotic behavior and the presence or absence of oscillation near the asymptotes.
A general form of a unitary sigmoid function is

  
    
      
        y
        =
        A
        
        S
        (
        f
        (
        x
        )
        )
        +
        B
        ,
      
    
    {\\displaystyle y=A\\,S(f(x))+B,}
  

where 
  
    
      
        S
      
    
    {\\displaystyle S}
  
 is an increasing sigmoid function, 
  
    
      
        f
        (
        x
        )
      
    
    {\\displaystyle f(x)}
  
 is a transformation of the independent variable, and 
  
    
      
        A
      
    
    {\\displaystyle A}
  
 and 
  
    
      
        B
      
    
    {\\displaystyle B}
  
 are constants controlling scaling and translation.


=== Classification ===


==== 1st kind ====
A unitary sigmoid function of the first kind is a bounded increasing function that approaches its lower and upper asymptotes monotonically, without oscillation. This class includes many of the standard sigmoid functions used in statistics, biomathematics, and engineering, such as the logistic function and related generalizations.


==== 2nd kind ====
A unitary sigmoid function of the second kind is a bounded increasing function that oscillates near the upper asymptote while preserving an overall sigmoid transition.


==== 3rd kind ====
A unitary sigmoid function of the third kind is a bounded increasing function that oscillates near both the lower and upper asymptotes. These functions retain the global shape of a sigmoid curve but exhibit oscillatory behavior in the vicinity of both limiting states.


=== Taxonomy ===
The tables below show the taxonomy of unitary sigmoid functions of all three kinds.
Table 1. Taxonomy matrix with examples of sigmoid functions of the 1st kind

Table 2. Taxonomy matrix with examples of sigmoid functions of the 2nd kind on the unbounded interval

Table 3. Taxonomy matrix with examples of sigmoid functions of the 3rd kind


=== Construction methods ===
The same theory presents a list of 30 methods for constructing sigmoid functions.. These include algebraic transformations, integration and convolution methods, constructions from bell-shaped functions, solutions of ordinary and partial differential equations, recursive schemes, stochastic differential equations, feedback systems, and chaotic systems.

M0: Construction method for sigmoid functions not evident or intuitive
M1: Inverse of singularity functions
M2: Sigmoid functions of embedded positive functions
M3: Rising a sigmoid function to the power
M4: Exponentiating a sigmoid function
M5: Symmetric sigmoid functions derived from asymmetric ones
M6: Sigmoid functions of the reciprocal independent variable
M7: Embedding a sigmoid function into other function
M8: Sum of sigmoid functions
M9: Multiplication of sigmoid functions
M10: Integral of the product of an increasing and a decreasing function
M11: Derivation from lambda (bell-shaped) functions
M12: Integration of lambda (bell-shaped) function
M13: Integration of the sum of lambda (bell-shaped) functions
M14: Integration of the product of two lambda (bell-shaped) functions
M15: Integration of the difference of two shifted sigmoid functions
M16: Integration of the product of two shifted sigmoid functions
M17: Convolution of sigmoid functions
M18: Integration of the product of lambda and sigmoid function
M19: Solutions of ordinary differential equations
M20: Solutions of partial differential equation (PDE)
M21: Solutions of functional differential equation (FDE)
M22: Sum of a sigmoid function and some derivatives
M23: Combination of sigmoid functions, its derivative and integral
M24: Filtering sigmoid functions
M25: Special cases of Gauss hypergeometric functions
M26: Feedback closed-loop systems
M27: Recursive functions
M28: Recursive time-delayed feed-forward loops
M29: Solutions of stochastic differential equation
M30: Chaotic sigmoid functions
Consult reference for more details.


== Definition ==
A sigmoid function is a bounded, differentiable, real function that is defined for all real input values and has a positive derivative at each point.


== Properties ==
In general, a sigmoid function is monotonic, and has a first derivative which is bell shaped. Conversely, the integral of any continuous, non-negative, bell-shaped function (with one local maximum and no local minimum, unless degenerate) will be sigmoidal. Thus the cumulative distribution functions for many common probability distributions are sigmoidal.""",
    tier=4,
    domain="computer_science",
    source="Wikipedia, 'Sigmoid function'",
    source_url="https://en.wikipedia.org/wiki/Sigmoid_function",
))

register_atom(Atom(
    atom_type="formula",
    name="cross_entropy",
    content="""In information theory, the cross-entropy between two probability distributions 
  
    
      
        p
      
    
    {\\displaystyle p}
  
 and 
  
    
      
        q
      
    
    {\\displaystyle q}
  
, over the same underlying set of events, measures the average number of bits needed to identify an event drawn from the set when the coding scheme used for the set is optimized for an estimated probability distribution 
  
    
      
        q
      
    
    {\\displaystyle q}
  
, rather than the true distribution 
  
    
      
        p
      
    
    {\\displaystyle p}
  
.


== Definition ==
The cross-entropy of the distribution 
  
    
      
        q
      
    
    {\\displaystyle q}
  
  relative to a distribution 
  
    
      
        p
      
    
    {\\displaystyle p}
  
 over a given set is defined as follows:

  
    
      
        H
        (
        p
        ,
        q
        )
        =
        −
        
          E
          
            p
          
        
        ⁡
        [
        log
        ⁡
        q
        ]
        ,
      
    
    {\\displaystyle H(p,q)=-\\operatorname {E} _{p}[\\log q],}
  

where 
  
    
      
        
          E
          
            p
          
        
        ⁡
        [
        ⋅
        ]
      
    
    {\\displaystyle \\operatorname {E} _{p}[\\cdot ]}
  
 is the expected value operator with respect to the distribution 
  
    
      
        p
      
    
    {\\displaystyle p}
  
.
The definition may be formulated using the Kullback–Leibler divergence 
  
    
      
        
          D
          
            
              K
              L
            
          
        
        (
        p
        ∥
        q
        )
      
    
    {\\displaystyle D_{\\mathrm {KL} }(p\\parallel q)}
  
, divergence of 
  
    
      
        p
      
    
    {\\displaystyle p}
  
 from 
  
    
      
        q
      
    
    {\\displaystyle q}
  
 (also known as the relative entropy of 
  
    
      
        p
      
    
    {\\displaystyle p}
  
 with respect to 
  
    
      
        q
      
    
    {\\displaystyle q}
  
).

  
    
      
        H
        (
        p
        ,
        q
        )
        =
        H
        (
        p
        )
        +
        
          D
          
            
              K
              L
            
          
        
        (
        p
        ∥
        q
        )
        ,
      
    
    {\\displaystyle H(p,q)=H(p)+D_{\\mathrm {KL} }(p\\parallel q),}
  

where 
  
    
      
        H
        (
        p
        )
      
    
    {\\displaystyle H(p)}
  
 is the entropy of 
  
    
      
        p
      
    
    {\\displaystyle p}
  
.
For discrete probability distributions 
  
    
      
        p
      
    
    {\\displaystyle p}
  
 and 
  
    
      
        q
      
    
    {\\displaystyle q}
  
 with the same support 
  
    
      
        
          
            X
          
        
      
    
    {\\displaystyle {\\mathcal {X}}}
  
, this means

The situation for continuous distributions is analogous. We have to assume that 
  
    
      
        p
      
    
    {\\displaystyle p}
  
 and 
  
    
      
        q
      
    
    {\\displaystyle q}
  
 are absolutely continuous with respect to some reference measure 
  
    
      
        r
      
    
    {\\displaystyle r}
  
 (usually 
  
    
      
        r
      
    
    {\\displaystyle r}
  
 is a Lebesgue measure on a Borel σ-algebra). Let 
  
    
      
        P
      
    
    {\\displaystyle P}
  
 and 
  
    
      
        Q
      
    
    {\\displaystyle Q}
  
 be probability density functions of 
  
    
      
        p
      
    
    {\\displaystyle p}
  
 and 
  
    
      
        q
      
    
    {\\displaystyle q}
  
 with respect to 
  
    
      
        r
      
    
    {\\displaystyle r}
  
. Then

  
    
      
        −
        
          ∫
          
            
              X
            
          
        
        P
        (
        x
        )
        
        log
        ⁡
        Q
        (
        x
        )
        
        
          d
        
        x
        =
        
          E
          
            p
          
        
        ⁡
        [
        −
        log
        ⁡
        Q
        ]
        ,
      
    
    {\\displaystyle -\\int _{\\mathcal {X}}P(x)\\,\\log Q(x)\\,\\mathrm {d} x=\\operatorname {E} _{p}[-\\log Q],}
  

and therefore

NB: The notation 
  
    
      
        H
        (
        p
        ,
        q
        )
      
    
    {\\displaystyle H(p,q)}
  
 is also used for a different concept, the joint entropy of 
  
    
      
        p
      
    
    {\\displaystyle p}
  
 and 
  
    
      
        q
      
    
    {\\displaystyle q}
  
.


== Motivation ==
In information theory, the Kraft–McMillan theorem establishes that any directly decodable coding scheme for coding a message to identify one value 
  
    
      
        
          x
          
            i
          
        
      
    
    {\\displaystyle x_{i}}
  
 out of a set of possibilities 
  
    
      
        {
        
          x
          
            1
          
        
        ,
        …
        ,
        
          x
          
            n
          
        
        }
      
    
    {\\displaystyle \\{x_{1},\\ldots ,x_{n}\\}}
  
 can be seen as representing an implicit probability distribution 
  
    
      
        q
        (
        
          x
          
            i
          
        
        )
        =
        
          
            (
            
              
                1
                2
              
            
            )
          
          
            
              ℓ
              
                i
              
            
          
        
      
    
    {\\displaystyle q(x_{i})=\\left({\\frac {1}{2}}\\right)^{\\ell _{i}}}
  
 over 
  
    
      
        {
        
          x
          
            1
          
        
        ,
        …
        ,
        
          x
          
            n
          
        
        }
      
    
    {\\displaystyle \\{x_{1},\\ldots ,x_{n}\\}}
  
, where 
  
    
      
        
          ℓ
          
            i
          
        
      
    
    {\\displaystyle \\ell _{i}}
  
 is the length of the code for 
  
    
      
        
          x
          
            i
          
        
      
    
    {\\displaystyle x_{i}}
  
 in bits. Therefore, cross-entropy can be interpreted as the expected message-length per datum when a wrong distribution 
  
    
      
        q
      
    
    {\\displaystyle q}
  
 is assumed while the data actually follows a distribution 
  
    
      
        p
      
    
    {\\displaystyle p}
  
.""",
    tier=4,
    domain="computer_science",
    source="Wikipedia, 'Cross-entropy'",
    source_url="https://en.wikipedia.org/wiki/Cross-entropy",
))

register_atom(Atom(
    atom_type="result",
    name="info_entropy",
    content="""In information theory, the entropy of a random variable quantifies the average level of uncertainty or information associated with the variable's potential states or possible outcomes. This measures the expected amount of information needed to describe the state of the variable, considering the distribution of probabilities across all potential states. Given a discrete random variable 
  
    
      
        X
      
    
    {\\displaystyle X}
  
, which may be any member 
  
    
      
        x
      
    
    {\\displaystyle x}
  
 within the set 
  
    
      
        
          
            X
          
        
      
    
    {\\displaystyle {\\mathcal {X}}}
  
 and is distributed according to 
  
    
      
        p
        :
        
          
            X
          
        
        →
        [
        0
        ,
        1
        ]
      
    
    {\\displaystyle p\\colon {\\mathcal {X}}\\to [0,1]}
  
, the entropy is

  
    
      
        
          H
        
        (
        X
        )
        :=
        −
        
          ∑
          
            x
            ∈
            
              
                X
              
            
          
        
        p
        (
        x
        )
        log
        ⁡
        p
        (
        x
        )
        ,
      
    
    {\\displaystyle \\mathrm {H} (X):=-\\sum _{x\\in {\\mathcal {X}}}p(x)\\log p(x),}
  

where 
  
    
      
        Σ
      
    
    {\\displaystyle \\Sigma }
  
 denotes the sum over the variable's possible values. The choice of base for 
  
    
      
        log
      
    
    {\\displaystyle \\log }
  
, the logarithm, varies for different applications. Base 2 gives the unit of bits (or "shannons"), while base e gives "natural units" nat, and base 10 gives units of "dits", "bans", or "hartleys". An equivalent definition of entropy is the expected value of the self-information of a variable.
The concept of information entropy was introduced by Claude Shannon in his 1948 paper "A Mathematical Theory of Communication", and is also referred to as Shannon entropy. Shannon's theory defines a data communication system composed of three elements: a source of data, a communication channel, and a receiver. The "fundamental problem of communication" – as expressed by Shannon – is for the receiver to be able to identify what data was generated by the source, based on the signal it receives through the channel. Shannon considered various ways to encode, compress, and transmit messages from a data source, and proved in his source coding theorem that the entropy represents an absolute mathematical limit on how well data from the source can be losslessly compressed onto a perfectly noiseless channel. Shannon strengthened this result considerably for noisy channels in his noisy-channel coding theorem.
Entropy in information theory is directly analogous to the entropy in statistical thermodynamics. The analogy results when the values of the random variable designate energies of microstates, so Gibbs's formula for the entropy is formally identical to Shannon's formula. Entropy has relevance to other areas of mathematics such as combinatorics and machine learning. The definition can be derived from a set of axioms establishing that entropy should be a measure of how informative the average outcome of a variable is. For a continuous random variable, differential entropy is analogous to entropy. The definition 
  
    
      
        
          E
        
        [
        −
        log
        ⁡
        p
        (
        X
        )
        ]
      
    
    {\\displaystyle \\mathbb {E} [-\\log p(X)]}
  
 generalizes the above.


== Introduction ==
The core idea of information theory is that the "informational value" of a communicated message depends on the degree to which the content of the message is surprising. If a highly likely event occurs, the message carries very little information. On the other hand, if a highly unlikely event occurs, the message is much more informative. For instance, the knowledge that some particular number will not be the winning number of a lottery provides very little information, because any particular chosen number will almost certainly not win. However, knowledge that a particular number will win a lottery has high informational value because it communicates the occurrence of a very low probability event.
The information content, also called the surprisal or self-information, of an event 
  
    
      
        E
      
    
    {\\displaystyle E}
  
 is a function that increases as the probability 
  
    
      
        p
        (
        E
        )
      
    
    {\\displaystyle p(E)}
  
 of an event decreases. When 
  
    
      
        p
        (
        E
        )
      
    
    {\\displaystyle p(E)}
  
 is close to 1, the surprisal of the event is low, but if 
  
    
      
        p
        (
        E
        )
      
    
    {\\displaystyle p(E)}
  
 is close to 0, the surprisal of the event is high. This relationship is described by the function

  
    
      
        log
        ⁡
        
          (
          
            
              1
              
                p
                (
                E
                )
              
            
          
          )
        
        ,
      
    
    {\\displaystyle \\log \\left({\\frac {1}{p(E)}}\\right),}
  

where 
  
    
      
        log
      
    
    {\\displaystyle \\log }
  
 is the logarithm, which gives 0 surprise when the probability of the event is 1. In fact, log is the only function that satisfies a specific set of conditions defined in section § Characterization.
Hence, we can define the information, or surprisal, of an event 
  
    
      
        E
      
    
    {\\displaystyle E}
  
 by

  
    
      
        I
        (
        E
        )
        =
        log
        ⁡
        
          (
          
            
              1
              
                p
                (
                E
                )
              
            
          
          )
        
        ,
      
    
    {\\displaystyle I(E)=\\log \\left({\\frac {1}{p(E)}}\\right),}
  

or equivalently,

  
    
      
        I
        (
        E
        )
        =
        −
        log
        ⁡
        (
        p
        (
        E
        )
        )
        .
      
    
    {\\displaystyle I(E)=-\\log(p(E)).}
  

Entropy measures the expected (i.e., average) amount of information conveyed by identifying the outcome of a random trial.  This implies that rolling a die has higher entropy than tossing a coin because each outcome of a single die roll has smaller probability (
  
    
      
        p
        =
        1
        
          /
        
        6
      
    
    {\\displaystyle p=1/6}
  
) than each outcome of a coin toss (
  
    
      
        p
        =
        1
        
          /
        
        2
      
    
    {\\displaystyle p=1/2}
  
).
Consider a coin with probability p of landing on heads and probability 1 − p of landing on tails. The maximum surprise is when p = 1/2, for which one outcome is not expected over the other. In this case a coin flip has an entropy of one bit (similarly, one trit with equiprobable values contains 
  
    
      
        
          log
          
            2
          
        
        ⁡
        3
      
    
    {\\displaystyle \\log _{2}3}
  
 (about 1.58496) bits of information because it can have one of three values). The minimum surprise is when p = 0 (impossibility) or p = 1 (certainty) and the entropy is zero bits. When the entropy is zero, there is no uncertainty at all – no freedom of choice – no information. Other values of p give entropies between zero and one bits.


=== Example ===
Information theory is useful to calculate the smallest amount of information required to convey a message, as in data compression.""",
    tier=5,
    domain="information_theory",
    source="Wikipedia, 'Entropy (information theory)'",
    source_url="https://en.wikipedia.org/wiki/Entropy_%28information_theory%29",
))

register_atom(Atom(
    atom_type="formula",
    name="softmax_eval",
    content="""The softmax function, also known as softargmax or normalized exponential function, converts a tuple of K real numbers into a probability distribution over K possible outcomes. It is a generalization of the logistic function to multiple dimensions, and is used in multinomial logistic regression. The softmax function is often used as the last activation function of a neural network to normalize the output of a network to a probability distribution over predicted output classes.


== Definition ==
The softmax function takes as input a tuple z of K real numbers, and normalizes it into a probability distribution consisting of K probabilities proportional to the exponentials of the input numbers. That is, prior to applying softmax, some tuple components could be negative, or greater than one; and might not sum to 1; but after applying softmax, each component will be in the interval 
  
    
      
        (
        0
        ,
        1
        )
      
    
    {\\displaystyle (0,1)}
  
, and the components will add up to 1, so that they can be interpreted as probabilities. Furthermore, the larger input components will correspond to larger probabilities.
Formally, the standard (unit) softmax function 
  
    
      
        σ
        :
        
          
            R
          
          
            K
          
        
        →
        (
        0
        ,
        1
        
          )
          
            K
          
        
      
    
    {\\displaystyle \\sigma :\\mathbb {R} ^{K}\\to (0,1)^{K}}
  
, where ⁠
  
    
      
        K
        >
        1
      
    
    {\\displaystyle K>1}
  
⁠, takes a tuple 
  
    
      
        
          z
        
        =
        (
        
          z
          
            1
          
        
        ,
        …
        ,
        
          z
          
            K
          
        
        )
        ∈
        
          
            R
          
          
            K
          
        
      
    
    {\\displaystyle \\mathbf {z} =(z_{1},\\dotsc ,z_{K})\\in \\mathbb {R} ^{K}}
  
 and computes each component of vector 
  
    
      
        σ
        (
        
          z
        
        )
        ∈
        (
        0
        ,
        1
        
          )
          
            K
          
        
      
    
    {\\displaystyle \\sigma (\\mathbf {z} )\\in (0,1)^{K}}
  
 with

  
    
      
        σ
        (
        
          z
        
        
          )
          
            i
          
        
        =
        
          
            
              e
              
                
                  z
                  
                    i
                  
                
              
            
            
              
                ∑
                
                  j
                  =
                  1
                
                
                  K
                
              
              
                e
                
                  
                    z
                    
                      j
                    
                  
                
              
            
          
        
        
        .
      
    
    {\\displaystyle \\sigma (\\mathbf {z} )_{i}={\\frac {e^{z_{i}}}{\\sum _{j=1}^{K}e^{z_{j}}}}\\,.}
  

In words, the softmax applies the standard exponential function to each element 
  
    
      
        
          z
          
            i
          
        
      
    
    {\\displaystyle z_{i}}
  
 of the input tuple 
  
    
      
        
          z
        
      
    
    {\\displaystyle \\mathbf {z} }
  
 (consisting of 
  
    
      
        K
      
    
    {\\displaystyle K}
  
 real numbers), and normalizes these values by dividing by the sum of all these exponentials. The normalization ensures that the sum of the components of the output vector 
  
    
      
        σ
        (
        
          z
        
        )
      
    
    {\\displaystyle \\sigma (\\mathbf {z} )}
  
 is 1. The term "softmax" derives from the amplifying effects of the exponential on any maxima in the input tuple. For example, the standard softmax of 
  
    
      
        (
        1
        ,
        2
        ,
        8
        )
      
    
    {\\displaystyle (1,2,8)}
  
 is approximately 
  
    
      
        (
        0.001
        ,
        0.002
        ,
        0.997
        )
      
    
    {\\displaystyle (0.001,0.002,0.997)}
  
, which amounts to assigning almost all of the total unit weight in the result to the position of the tuple's maximal element (of 8).
In general, instead of e a different base b > 0 can be used.  As above, if b > 1 then larger input components will result in larger output probabilities, and increasing the value of b will create probability distributions that are more concentrated around the positions of the largest input values. Conversely, if 0 < b < 1 then smaller input components will result in larger output probabilities, and decreasing the value of b will create probability distributions that are more concentrated around the positions of the smallest input values. Writing 
  
    
      
        b
        =
        
          e
          
            β
          
        
      
    
    {\\displaystyle b=e^{\\beta }}
  
 or 
  
    
      
        b
        =
        
          e
          
            −
            β
          
        
      
    
    {\\displaystyle b=e^{-\\beta }}
  
 (for real β) yields the expressions:

  
    
      
        σ
        (
        
          z
        
        
          )
          
            i
          
        
        =
        
          
            
              e
              
                β
                
                  z
                  
                    i
                  
                
              
            
            
              
                ∑
                
                  j
                  =
                  1
                
                
                  K
                
              
              
                e
                
                  β
                  
                    z
                    
                      j
                    
                  
                
              
            
          
        
        
           or 
        
        σ
        (
        
          z
        
        
          )
          
            i
          
        
        =
        
          
            
              e
              
                −
                β
                
                  z
                  
                    i
                  
                
              
            
            
              
                ∑
                
                  j
                  =
                  1
                
                
                  K
                
              
              
                e
                
                  −
                  β
                  
                    z
                    
                      j
                    
                  
                
              
            
          
        
        
           for 
        
        i
        =
        1
        ,
        …
        ,
        K
        .
      
    
    {\\displaystyle \\sigma (\\mathbf {z} )_{i}={\\frac {e^{\\beta z_{i}}}{\\sum _{j=1}^{K}e^{\\beta z_{j}}}}{\\text{ or }}\\sigma (\\mathbf {z} )_{i}={\\frac {e^{-\\beta z_{i}}}{\\sum _{j=1}^{K}e^{-\\beta z_{j}}}}{\\text{ for }}i=1,\\dotsc ,K.}
  

A value proportional to the reciprocal of β is sometimes referred to as the temperature: 
  
    
      
        β
        =
        1
        
          /
        
        k
        T
      
    
    {\\textstyle \\beta =1/kT}
  
, where k is typically 1 or the Boltzmann constant and T is the temperature. A higher temperature results in a more uniform output distribution (i.e.""",
    tier=5,
    domain="computer_science",
    source="Wikipedia, 'Softmax function'",
    source_url="https://en.wikipedia.org/wiki/Softmax_function",
))

register_atom(Atom(
    atom_type="formula",
    name="attention_score",
    content="""In machine learning, attention is a method that determines the importance of each component in a sequence relative to the other components in that sequence. In natural language processing, importance is represented by "soft" weights assigned to each word in a sentence. More generally, attention encodes vectors called token embeddings across a fixed-width sequence that can range from tens to millions of tokens in size.
Unlike "hard" weights, which are computed during the backwards training pass, "soft" weights exist only in the forward pass and therefore change with every step of the input. Earlier designs implemented the attention mechanism in a serial recurrent neural network (RNN) language translation system, but a more recent design, namely the transformer, removed the slower sequential RNN and relied more heavily on the faster parallel attention scheme.
Inspired by ideas about attention in humans, the attention mechanism was developed to address the weaknesses of using information from the hidden layers of recurrent neural networks. Recurrent neural networks favor information contained in words at the end of a sentence and thus deemed more recent, thereby tending to attenuate the significance and associated predictive weight assigned to information earlier in the sentence. Attention allows a token equal access to any part of a sentence directly, rather than only through the previous state.


== History ==

Additional surveys of the attention mechanism in deep learning are provided by Niu et al. and Soydaner.
The major breakthrough came with self-attention, where each element in the input sequence attends to all others, enabling the model to capture global dependencies. This idea was central to the Transformer architecture, which replaced recurrence with attention mechanisms. As a result, Transformers became the foundation for models like BERT, T5 and generative pre-trained transformers (GPT).


== Overview ==

The modern era of machine attention was revitalized by grafting an attention mechanism (Fig 1.  orange) to an Encoder-Decoder.

Figure 2 shows the internal step-by-step operation of the attention block (A) in Fig 1.


=== Interpreting attention weights ===
In translating between languages, alignment is the process of matching words from the source sentence to words of the translated sentence. Networks that perform verbatim translation without regard to word order would show the highest scores along the (dominant) diagonal of the matrix. The off-diagonal dominance shows that the attention mechanism is more nuanced.
Consider an example of translating I love you to French. On the first pass through the decoder, 94% of the attention weight is on the first English word I, so the network offers the word je. On the second pass of the decoder, 88% of the attention weight is on the third English word you, so it offers t'. On the last pass, 95% of the attention weight is on the second English word love, so it offers aime.
In the I love you example, the second word love is aligned with the third word aime. Stacking soft row vectors together for je, t', and aime yields an alignment matrix:

Sometimes, alignment can be multiple-to-multiple. For example, the English phrase look it up corresponds to cherchez-le. Thus, "soft" attention weights work better than "hard" attention weights (setting one attention weight to 1, and the others to 0), as we would like the model to make a context vector consisting of a weighted sum of the hidden vectors, rather than "the best one", as there may not be a best hidden vector.


== Variants ==

Many variants of attention implement soft weights, such as

fast weight programmers, or fast weight controllers (1992). A "slow" neural network outputs the "fast" weights of another neural network through outer products. The slow network learns by gradient descent. It was later renamed as "linearized self-attention".
Bahdanau-style attention, also referred to as additive attention,
Luong-style attention, which is known as multiplicative attention,
Early attention mechanisms similar to modern self-attention were proposed using recurrent neural networks. However, the highly parallelizable self-attention was introduced in 2017 and successfully used in the Transformer model,
positional attention and factorized positional attention.
For convolutional neural networks, attention mechanisms can be distinguished by the dimension on which they operate, namely: spatial attention, channel attention, or combinations.
These variants recombine the encoder-side inputs to redistribute those effects to each target output. Often, a correlation-style matrix of dot products provides the re-weighting coefficients.  In the figures below, W is the matrix of context attention weights, similar to the formula in Overview section above.


== Optimizations ==


=== Flash attention ===
The size of the attention matrix is proportional to the square of the number of input tokens. Therefore, when the input is long, calculating the attention matrix requires a lot of GPU memory. Flash attention is an implementation that reduces the memory needs and increases efficiency without sacrificing accuracy. It achieves this by partitioning the attention computation into smaller blocks that fit into the GPU's faster on-chip memory, reducing the need to store large intermediate matrices and thus lowering memory usage while increasing computational efficiency.


=== FlexAttention ===
FlexAttention is an attention kernel developed by Meta that allows users to modify attention scores prior to softmax and dynamically chooses the optimal attention algorithm.


== Applications ==
Attention is widely used in natural language processing, computer vision, and speech recognition. In NLP, it improves context understanding in tasks like question answering and summarization. In vision, visual attention helps models focus on relevant image regions, enhancing object detection and image captioning.


=== Attention maps as explanations for vision transformers ===

From the original paper on vision transformers (ViT), visualizing attention scores as a heat map (called saliency maps or attention maps) has become an important and routine way to inspect the decision making process of ViT models. One can compute the attention maps with respect to any attention head at any layer, while the deeper layers tend to show more semantically meaningful visualization. Attention rollout is a recursive algorithm to combine attention scores across all layers, by computing the dot product of successive attention maps.
Because vision transformers are typically trained in a self-supervised manner, attention maps are generally not class-sensitive. When a classification head is attached to the ViT backbone, class-discriminative attention maps (CDAM) combines attention maps and gradients with respect to the class [CLS] token. Some class-sensitive interpretability methods originally developed for convolutional neural networks can be also applied to ViT, such as GradCAM, which back-propagates the gradients to the outputs of the final attention layer.
Using attention as basis of explanation for the transformers in language and vision is not without debate.""",
    tier=5,
    domain="computer_science",
    source="Wikipedia, 'Attention (machine learning)'",
    source_url="https://en.wikipedia.org/wiki/Attention_%28machine_learning%29",
))

register_atom(Atom(
    atom_type="formula",
    name="backprop_simple",
    content="""In machine learning, backpropagation is a gradient computation method commonly used for training a neural network in computing parameter updates.
It is an efficient application of the chain rule to neural networks. Backpropagation efficiently computes the gradient of the loss with respect to the network weights for a single input–output example. It does this by propagating derivatives backward, one layer at a time, from the output layer to the input layer, thereby avoiding redundant chain-rule calculations.
Strictly speaking, the term backpropagation refers only to an algorithm for efficiently computing the gradient, not how the gradient is used, but the term is often used loosely to refer to the entire learning algorithm. This includes changing model parameters in the negative direction of the gradient, such as by stochastic gradient descent, or as an intermediate step in a more complicated optimizer, such as Adaptive Moment Estimation.
Backpropagation had multiple discoveries and partial discoveries, with a tangled history and terminology (see § History). Some other names for the technique include "reverse mode of automatic differentiation" or "reverse accumulation".


== Overview ==
Backpropagation computes the gradient in weight space of a feedforward neural network, with respect to a loss function. Denote:

  
    
      
        x
      
    
    {\\displaystyle x}
  
: input (vector of features)

  
    
      
        y
      
    
    {\\displaystyle y}
  
: target output
For classification, output will be a vector of class probabilities (e.g., 
  
    
      
        (
        0.1
        ,
        0.7
        ,
        0.2
        )
      
    
    {\\displaystyle (0.1,0.7,0.2)}
  
, and target output is a specific class, encoded by the one-hot/dummy variable (e.g., 
  
    
      
        (
        0
        ,
        1
        ,
        0
        )
      
    
    {\\displaystyle (0,1,0)}
  
).

  
    
      
        C
      
    
    {\\displaystyle C}
  
: loss function or "cost function"
For classification, this is usually cross-entropy (XC, log loss), while for regression it is usually squared error loss (SEL).

  
    
      
        L
      
    
    {\\displaystyle L}
  
: the number of layers

  
    
      
        
          W
          
            l
          
        
        =
        (
        
          w
          
            j
            k
          
          
            l
          
        
        )
      
    
    {\\displaystyle W^{l}=(w_{jk}^{l})}
  
: the weights between layer 
  
    
      
        l
        −
        1
      
    
    {\\displaystyle l-1}
  
 and 
  
    
      
        l
      
    
    {\\displaystyle l}
  
, where 
  
    
      
        
          w
          
            j
            k
          
          
            l
          
        
      
    
    {\\displaystyle w_{jk}^{l}}
  
 is the weight between the 
  
    
      
        k
      
    
    {\\displaystyle k}
  
-th node in layer 
  
    
      
        l
        −
        1
      
    
    {\\displaystyle l-1}
  
 and the 
  
    
      
        j
      
    
    {\\displaystyle j}
  
-th node in layer 
  
    
      
        l
      
    
    {\\displaystyle l}
  

  
    
      
        
          f
          
            l
          
        
      
    
    {\\displaystyle f^{l}}
  
: activation functions at layer 
  
    
      
        l
      
    
    {\\displaystyle l}
  

For classification the last layer is usually the logistic function for binary classification, and softmax (softargmax) for multi-class classification, while for the hidden layers this was traditionally a sigmoid function (logistic function or others) on each node (coordinate), but today is more varied, with rectifier (ramp, ReLU) being common.

  
    
      
        
          a
          
            j
          
          
            l
          
        
      
    
    {\\displaystyle a_{j}^{l}}
  
: activation of the 
  
    
      
        j
      
    
    {\\displaystyle j}
  
-th node in layer 
  
    
      
        l
      
    
    {\\displaystyle l}
  
.
In the derivation of backpropagation, other intermediate quantities are used by introducing them as needed below. Bias terms are not treated specially since they correspond to a weight with a fixed input of 1. For backpropagation the specific loss function and activation functions do not matter as long as they and their derivatives can be evaluated efficiently. Traditional activation functions include sigmoid, tanh, ReLU, Swish, Mish,, and many others.
The overall network is a combination of function composition and matrix multiplication:

  
    
      
        g
        (
        x
        )
        :=
        
          f
          
            L
          
        
        (
        
          W
          
            L
          
        
        
          f
          
            L
            −
            1
          
        
        (
        
          W
          
            L
            −
            1
          
        
        ⋯
        
          f
          
            1
          
        
        (
        
          W
          
            1
          
        
        x
        )
        ⋯
        )
        )
      
    
    {\\displaystyle g(x):=f^{L}(W^{L}f^{L-1}(W^{L-1}\\cdots f^{1}(W^{1}x)\\cdots ))}
  

For a training set there will be a set of input–output pairs, 
  
    
      
        
          {
          
            (
            
              x
              
                i
              
            
            ,
            
              y
              
                i
              
            
            )
          
          }
        
      
    
    {\\displaystyle \\left\\{(x_{i},y_{i})\\right\\}}
  
. For each input–output pair 
  
    
      
        (
        
          x
          
            i
          
        
        ,
        
          y
          
            i
          
        
        )
      
    
    {\\displaystyle (x_{i},y_{i})}
  
 in the training set, the loss of the model on that pair is the cost of the difference between the predicted output 
  
    
      
        g
        (
        
          x
          
            i
          
        
        )
      
    
    {\\displaystyle g(x_{i})}
  
 and the target output 
  
    
      
        
          y
          
            i
          
        
      
    
    {\\displaystyle y_{i}}
  
:

  
    
      
        C
        (
        
          y
          
            i
          
        
        ,
        g
        (
        
          x
          
            i
          
        
        )
        )
      
    
    {\\displaystyle C(y_{i},g(x_{i}))}
  

Note the distinction: during model evaluation the weights are fixed while the inputs vary (and the target output may be unknown), and the network ends with the output layer (it does not include the loss function). During model training the input–output pair is fixed while the weights vary, and the network ends with the loss function.
Backpropagation computes the gradient for a fixed input–output pair 
  
    
      
        (
        
          x
          
            i
          
        
        ,
        
          y
          
            i
          
        
        )
      
    
    {\\displaystyle (x_{i},y_{i})}
  
, where the weights 
  
    
      
        
          w
          
            j
            k
          
          
            l
          
        
      
    
    {\\displaystyle w_{jk}^{l}}
  
 can vary.""",
    tier=5,
    domain="computer_science",
    source="Wikipedia, 'Backpropagation'",
    source_url="https://en.wikipedia.org/wiki/Backpropagation",
))

register_atom(Atom(
    atom_type="algorithm",
    name="neural_forward",
    content="""A feedforward neural network is an artificial neural network in which information flows in a single direction – inputs are multiplied by weights to obtain outputs (inputs-to-output). It contrasts with a recurrent neural network, in which loops allow information from later processing stages to feed back to earlier stages. Feedforward multiplication is essential for backpropagation, because feedback, where the outputs feed back to the very same inputs and modify them, forms an infinite loop which is not possible to differentiate through backpropagation. This nomenclature appears to be a point of confusion between some computer scientists and scientists in other fields studying brain networks.


== Mathematical foundations ==


=== Activation function ===
The two historically common activation functions are both sigmoids, and are described by

  
    
      
        y
        (
        
          v
          
            i
          
        
        )
        =
        tanh
        ⁡
        (
        
          v
          
            i
          
        
        )
         
         
        
          and
        
         
         
        y
        (
        
          v
          
            i
          
        
        )
        =
        (
        1
        +
        
          e
          
            −
            
              v
              
                i
              
            
          
        
        
          )
          
            −
            1
          
        
        .
      
    
    {\\displaystyle y(v_{i})=\\tanh(v_{i})~~{\\text{and}}~~y(v_{i})=(1+e^{-v_{i}})^{-1}.}
  

The first is a hyperbolic tangent that ranges from -1 to 1, while the other is the logistic function, which is similar in shape but ranges from 0 to 1. Here 
  
    
      
        
          y
          
            i
          
        
      
    
    {\\displaystyle y_{i}}
  
 is the output of the 
  
    
      
        i
      
    
    {\\displaystyle i}
  
-th node (neuron) and 
  
    
      
        
          v
          
            i
          
        
      
    
    {\\displaystyle v_{i}}
  
 is the weighted sum of the input connections. Alternative activation functions have been proposed, including the rectifier and softplus functions. More specialized activation functions include radial basis functions (used in radial basis networks, another class of supervised neural network models).
In recent developments of deep learning, the rectified linear unit (ReLU) is more frequently used as one of the possible ways to overcome the numerical problems related to the sigmoids.


=== Learning ===

Learning occurs by changing connection weights after each piece of data is processed, based on the amount of error in the output compared to the expected result. This is an example of supervised learning, and is carried out through backpropagation.
We can represent the degree of error in an output node 
  
    
      
        j
      
    
    {\\displaystyle j}
  
 in the 
  
    
      
        n
      
    
    {\\displaystyle n}
  
-th data point (training example) by 
  
    
      
        
          e
          
            j
          
        
        (
        n
        )
        =
        
          d
          
            j
          
        
        (
        n
        )
        −
        
          y
          
            j
          
        
        (
        n
        )
      
    
    {\\displaystyle e_{j}(n)=d_{j}(n)-y_{j}(n)}
  
, where 
  
    
      
        
          d
          
            j
          
        
        (
        n
        )
      
    
    {\\displaystyle d_{j}(n)}
  
 is the desired target value for 
  
    
      
        n
      
    
    {\\displaystyle n}
  
-th data point at node 
  
    
      
        j
      
    
    {\\displaystyle j}
  
, and 
  
    
      
        
          y
          
            j
          
        
        (
        n
        )
      
    
    {\\displaystyle y_{j}(n)}
  
 is the value produced at node 
  
    
      
        j
      
    
    {\\displaystyle j}
  
 when the 
  
    
      
        n
      
    
    {\\displaystyle n}
  
-th data point is given as an input.
The node weights can then be adjusted based on corrections that minimize the error in the entire output for the 
  
    
      
        n
      
    
    {\\displaystyle n}
  
-th data point, given by

  
    
      
        
          
            E
          
        
        (
        n
        )
        =
        
          
            1
            2
          
        
        
          ∑
          
            
              output node 
            
            j
          
        
        
          e
          
            j
          
          
            2
          
        
        (
        n
        )
        .
      
    
    {\\displaystyle {\\mathcal {E}}(n)={\\frac {1}{2}}\\sum _{{\\text{output node }}j}e_{j}^{2}(n).}
  

Using gradient descent, the change in each weight 
  
    
      
        
          w
          
            i
            j
          
        
      
    
    {\\displaystyle w_{ij}}
  
 is

  
    
      
        Δ
        
          w
          
            j
            i
          
        
        (
        n
        )
        =
        −
        η
        
          
            
              ∂
              
                
                  E
                
              
              (
              n
              )
            
            
              ∂
              
                v
                
                  j
                
              
              (
              n
              )
            
          
        
        
          y
          
            i
          
        
        (
        n
        )
      
    
    {\\displaystyle \\Delta w_{ji}(n)=-\\eta {\\frac {\\partial {\\mathcal {E}}(n)}{\\partial v_{j}(n)}}y_{i}(n)}
  

where 
  
    
      
        
          y
          
            i
          
        
        (
        n
        )
      
    
    {\\displaystyle y_{i}(n)}
  
 is the output of the previous neuron 
  
    
      
        i
      
    
    {\\displaystyle i}
  
, and 
  
    
      
        η
      
    
    {\\displaystyle \\eta }
  
 is the learning rate, which is selected to ensure that the weights quickly converge to a response, without oscillations. In the previous expression, 
  
    
      
        
          
            
              ∂
              
                
                  E
                
              
              (
              n
              )
            
            
              ∂
              
                v
                
                  j
                
              
              (
              n
              )
            
          
        
      
    
    {\\displaystyle {\\frac {\\partial {\\mathcal {E}}(n)}{\\partial v_{j}(n)}}}
  
 denotes the partial derivative of the error 
  
    
      
        
          
            E
          
        
        (
        n
        )
      
    
    {\\displaystyle {\\mathcal {E}}(n)}
  
 according to the weighted sum 
  
    
      
        
          v
          
            j
          
        
        (
        n
        )
      
    
    {\\displaystyle v_{j}(n)}
  
 of the input connections of neuron 
  
    
      
        i
      
    
    {\\displaystyle i}
  
.
The derivative to be calculated depends on the induced local field 
  
    
      
        
          v
          
            j
          
        
      
    
    {\\displaystyle v_{j}}
  
, which itself varies.""",
    tier=6,
    domain="computer_science",
    source="Wikipedia, 'Feedforward neural network'",
    source_url="https://en.wikipedia.org/wiki/Feedforward_neural_network",
))

register_atom(Atom(
    atom_type="definition",
    name="big_o",
    content="""Big O notation is a mathematical notation that describes the approximate size of a function on a domain. Big O is a member of a family of notations invented by the German mathematicians Paul Bachmann and Edmund Landau and expanded by others, collectively called Bachmann–Landau notation. The letter O stands for Ordnung, that is, the order of approximation.
In computer science, big O notation is used to classify algorithms by how their run time or space requirements grow with the input. In analytic number theory, big O notation expresses bounds on the growth of an arithmetical function, as for the remainder term in the prime number theorem.
In mathematical analysis, including calculus, Big O notation bounds the error when truncating a power series and expresses the quality
of approximation of a real or complex valued function by a simpler function.
Often, big O notation characterizes functions according to their growth rates as the variable becomes large: different functions with the same asymptotic growth rate may be represented using the same O notation. The letter O is used because the growth rate of a function is also referred to as the order of the function. A description of a function in terms of big O notation only provides an upper bound on the growth rate of the function.
Associated with big O notation are several related notations, using the symbols 
  
    
      
        o
      
    
    {\\displaystyle o}
  
, 
  
    
      
        ∼
      
    
    {\\displaystyle \\sim }
  
, 
  
    
      
        Ω
      
    
    {\\displaystyle \\Omega }
  
, 
  
    
      
        ≪
      
    
    {\\displaystyle \\ll }
  
, 
  
    
      
        ≫
      
    
    {\\displaystyle \\gg }
  
, 
  
    
      
        ≍
      
    
    {\\displaystyle \\asymp }
  
, 
  
    
      
        ω
      
    
    {\\displaystyle \\omega }
  
, and 
  
    
      
        Θ
      
    
    {\\displaystyle \\Theta }
  
 to describe other kinds of bounds on growth rates. 
Bachmann proposed the notation in 1894 and Landau extended it in 1909. An earlier notation was proposed by Paul du Bois-Reymond in 1870.


== Formal definition ==
Let 
  
    
      
        f
        ,
      
    
    {\\textstyle f,}
  
 the function to be estimated, be either a real or complex valued function defined on a domain 
  
    
      
        D
        ,
      
    
    {\\textstyle D,}
  
 and let 
  
    
      
        g
        ,
      
    
    {\\textstyle g,}
  
 the comparison function, be a non-negative real valued function defined on the same set 
  
    
      
        D
        .
      
    
    {\\textstyle D.}
  
 Common choices for the domain are intervals of real numbers, bounded or unbounded, the set of positive integers, the set of complex numbers and tuples of real/complex numbers. With the domain written explicitly or understood implicitly, one writes

  
    
      
        f
        (
        x
        )
        =
        O
        
          
            (
          
        
        g
        (
        x
        )
        
          
            )
          
        
         
      
    
    {\\displaystyle f(x)=O{\\bigl (}g(x){\\bigr )}\\ }
  

which is read as  "
  
    
      
        f
        (
        x
        )
      
    
    {\\textstyle f(x)}
  
 is big 
  
    
      
        O
      
    
    {\\textstyle O}
  
 of 
  
    
      
        g
        (
        x
        )
      
    
    {\\textstyle g(x)}
  
"  if there exists a positive real number 
  
    
      
        M
      
    
    {\\textstyle M}
  
 such that

  
    
      
        
          |
          
            f
            (
            x
            )
          
          |
        
        ≤
        M
         
        g
        (
        x
        )
        
         
        
          
             
            f
            o
            r
             
            a
            l
            l
             
          
        
         
        
        x
        ∈
        D
        .
      
    
    {\\displaystyle \\left|f(x)\\right|\\leq M\\ g(x)\\qquad ~{\\mathsf {\\ for\\ all\\ }}~\\quad x\\in D.}
  

If 
  
    
      
        g
        (
        x
        )
        >
        0
      
    
    {\\displaystyle g(x)>0}
  
 (i.e. g is also never zero) throughout the domain 
  
    
      
        D
        ,
      
    
    {\\displaystyle D,}
  
 an equivalent definition is that the ratio 
  
    
      
        
          
            
              f
              (
              x
              )
            
            
              g
              (
              x
              )
            
          
        
      
    
    {\\textstyle {\\frac {f(x)}{g(x)}}}
  
 is bounded, i.e. there is a positive real number 
  
    
      
        M
      
    
    {\\displaystyle M}
  
 so that 
  
    
      
        
          
            |
          
        
        
          
            
              f
              (
              x
              )
            
            
              g
              (
              x
              )
            
          
        
        
          
            |
          
        
        ≤
        M
      
    
    {\\textstyle {\\Big |}{\\frac {f(x)}{g(x)}}{\\Big |}\\leq M}
  
 for all 
  
    
      
        x
        ∈
        D
        .
      
    
    {\\displaystyle x\\in D.}
  
 These encompass all the uses of  big 
  
    
      
        O
      
    
    {\\textstyle O}
  
  in computer science and mathematics, including its use where the domain is finite, infinite, real, complex, single variate, or multivariate. In most applications, one chooses the function 
  
    
      
        g
        (
        x
        )
      
    
    {\\displaystyle g(x)}
  
 appearing within the argument of 
  
    
      
        O
        
          
            (
          
        
        ⋅
        
          
            )
          
        
      
    
    {\\textstyle O{\\bigl (}\\cdot {\\bigr )}}
  
 to be as simple a form as possible, omitting constant factors and lower order terms. The number 
  
    
      
        M
      
    
    {\\textstyle M}
  
 is called the implied constant because it is normally not specified. When using big 
  
    
      
        O
      
    
    {\\textstyle O}
  
 notation, what matters is that some finite 
  
    
      
        M
      
    
    {\\displaystyle M}
  
 exists, not its specific value. This simplifies the presentation of many analytic inequalities.
For functions defined on positive real numbers or positive integers, a more restrictive and somewhat conflicting definition
is still in common use, especially in computer science.""",
    tier=4,
    domain="computer_science",
    source="Wikipedia, 'Big O notation'",
    source_url="https://en.wikipedia.org/wiki/Big_O_notation",
))

register_atom(Atom(
    atom_type="formula",
    name="convolution",
    content="""In mathematics (in particular, functional analysis), convolution is a mathematical operation on two functions 
  
    
      
        f
      
    
    {\\displaystyle f}
  
 and 
  
    
      
        g
      
    
    {\\displaystyle g}
  
 that produces a third function 
  
    
      
        f
        ∗
        g
      
    
    {\\displaystyle f*g}
  
, as the integral of the product of the two functions after one is reflected about the y-axis and shifted. The term convolution refers to both the resulting function and to the process of computing it. The integral is evaluated for all values of shift, producing the convolution function. The choice of which function is reflected and shifted before the integral does not change the integral result (see commutativity). Graphically, it expresses how the 'shape' of one function is modified by the other.
Some features of convolution are similar to cross-correlation: for real-valued functions, of a continuous or discrete variable, convolution 
  
    
      
        f
        ∗
        g
      
    
    {\\displaystyle f*g}
  
 differs from cross-correlation 
  
    
      
        f
        ⋆
        g
      
    
    {\\displaystyle f\\star g}
  
 only in that either 
  
    
      
        f
        (
        x
        )
      
    
    {\\displaystyle f(x)}
  
 or 
  
    
      
        g
        (
        x
        )
      
    
    {\\displaystyle g(x)}
  
 is reflected about the y-axis in convolution; thus it is a cross-correlation of 
  
    
      
        g
        (
        −
        x
        )
      
    
    {\\displaystyle g(-x)}
  
 and 
  
    
      
        f
        (
        x
        )
      
    
    {\\displaystyle f(x)}
  
, or 
  
    
      
        f
        (
        −
        x
        )
      
    
    {\\displaystyle f(-x)}
  
 and 
  
    
      
        g
        (
        x
        )
      
    
    {\\displaystyle g(x)}
  
. For complex-valued functions, the cross-correlation operator is the adjoint of the convolution operator.
Convolution has applications that include probability, statistics, acoustics, spectroscopy, signal processing and image processing, computer vision and human vision, geophysics, engineering, physics, and differential equations.
The convolution can be defined for functions on Euclidean space and other groups (as algebraic structures). For example, periodic functions, such as the discrete-time Fourier transform, can be defined on a circle and convolved by periodic convolution. (See row 18 at DTFT § Properties.) A discrete convolution can be defined for functions on the set of integers.
Generalizations of convolution have applications in the field of numerical analysis and numerical linear algebra, and in the design and implementation of finite impulse response filters in signal processing.
Computing the inverse of the convolution operation is known as deconvolution.


== Definition ==
The convolution of 
  
    
      
        f
      
    
    {\\displaystyle f}
  
 and 
  
    
      
        g
      
    
    {\\displaystyle g}
  
 is written 
  
    
      
        f
        ∗
        g
      
    
    {\\displaystyle f*g}
  
, denoting the operator with the symbol 
  
    
      
        ∗
      
    
    {\\displaystyle *}
  
. It is defined as the integral of the product of the two functions after one is reflected about the y-axis and shifted. As such, it is a particular kind of integral transform:

  
    
      
        (
        f
        ∗
        g
        )
        (
        t
        )
        :=
        
          ∫
          
            −
            ∞
          
          
            ∞
          
        
        f
        (
        τ
        )
        g
        (
        t
        −
        τ
        )
        
        d
        τ
        .
      
    
    {\\displaystyle (f*g)(t):=\\int _{-\\infty }^{\\infty }f(\\tau )g(t-\\tau )\\,d\\tau .}
  

An equivalent definition is (see commutativity):

  
    
      
        (
        f
        ∗
        g
        )
        (
        t
        )
        :=
        
          ∫
          
            −
            ∞
          
          
            ∞
          
        
        f
        (
        t
        −
        τ
        )
        g
        (
        τ
        )
        
        d
        τ
        .
      
    
    {\\displaystyle (f*g)(t):=\\int _{-\\infty }^{\\infty }f(t-\\tau )g(\\tau )\\,d\\tau .}
  

While the symbol 
  
    
      
        t
      
    
    {\\displaystyle t}
  
 is used above, it need not represent the time domain. At each 
  
    
      
        t
      
    
    {\\displaystyle t}
  
, the convolution formula can be described as the area under the function 
  
    
      
        f
        (
        τ
        )
      
    
    {\\displaystyle f(\\tau )}
  
 weighted by the function 
  
    
      
        g
        (
        −
        τ
        )
      
    
    {\\displaystyle g(-\\tau )}
  
 shifted by the amount 
  
    
      
        t
      
    
    {\\displaystyle t}
  
.""",
    tier=5,
    domain="computer_science",
    source="Wikipedia, 'Convolution'",
    source_url="https://en.wikipedia.org/wiki/Convolution",
))

register_atom(Atom(
    atom_type="formula",
    name="polynomial_hash",
    content="""A rolling hash (also known as recursive hashing or rolling checksum) is a hash function where the input is hashed in a window that moves through the input.
A few hash functions allow a rolling hash to be computed very quickly—the new hash value is rapidly calculated given only the old hash value, the old value removed from the window, and the new value added to the window—similar to the way a moving average function can be computed much more quickly than other low-pass filters; and similar to the way a Zobrist hash can be rapidly updated from the old hash value.
One of the main applications is the Rabin–Karp string search algorithm, which uses the rolling hash described below. Another popular application is the rsync program, which uses a checksum based on Mark Adler's adler-32 as its rolling hash. Low Bandwidth Network Filesystem (LBFS) uses a Rabin fingerprint as its rolling hash. FastCDC (Fast Content-Defined Chunking) uses a compute-efficient Gear fingerprint as its rolling hash.
At best, rolling hash values are pairwise independent or strongly universal. They cannot be 3-wise independent, for example.


== Polynomial rolling hash ==
The Rabin–Karp string search algorithm is often explained using a rolling hash function that only uses multiplications and additions:

  
    
      
        H
        =
        
          c
          
            1
          
        
        
          a
          
            k
            −
            1
          
        
        +
        
          c
          
            2
          
        
        
          a
          
            k
            −
            2
          
        
        +
        
          c
          
            3
          
        
        
          a
          
            k
            −
            3
          
        
        +
        .
        .
        .
        +
        
          c
          
            k
          
        
        
          a
          
            0
          
        
      
    
    {\\displaystyle H=c_{1}a^{k-1}+c_{2}a^{k-2}+c_{3}a^{k-3}+...+c_{k}a^{0}}
  
,
where 
  
    
      
        a
      
    
    {\\displaystyle a}
  
 is a constant, and 
  
    
      
        
          c
          
            1
          
        
        ,
        .
        .
        .
        ,
        
          c
          
            k
          
        
      
    
    {\\displaystyle c_{1},...,c_{k}}
  
 are the input characters (but this function is not a Rabin fingerprint, see below).
In order to avoid manipulating huge 
  
    
      
        H
      
    
    {\\displaystyle H}
  
 values, all math is done modulo 
  
    
      
        n
      
    
    {\\displaystyle n}
  
. The choice of 
  
    
      
        a
      
    
    {\\displaystyle a}
  
 and 
  
    
      
        n
      
    
    {\\displaystyle n}
  
 is critical to get good hashing; in particular, the modulus 
  
    
      
        n
      
    
    {\\displaystyle n}
  
 is typically a prime number.  See linear congruential generator for more discussion.
Removing and adding characters simply involves adding or subtracting the first or last term. Shifting all characters by one position to the left requires multiplying the entire sum 
  
    
      
        H
      
    
    {\\displaystyle H}
  
 by 
  
    
      
        a
      
    
    {\\displaystyle a}
  
. Shifting all characters by one position to the right requires dividing the entire sum 
  
    
      
        H
      
    
    {\\displaystyle H}
  
 by 
  
    
      
        a
      
    
    {\\displaystyle a}
  
. Note that in modulo arithmetic, 
  
    
      
        a
      
    
    {\\displaystyle a}
  
 can be chosen to have a multiplicative inverse 
  
    
      
        
          a
          
            −
            1
          
        
      
    
    {\\displaystyle a^{-1}}
  
 by which 
  
    
      
        H
      
    
    {\\displaystyle H}
  
 can be multiplied to get the result of the division without actually performing a division.


== Rabin fingerprint ==
The Rabin fingerprint is another hash, which also interprets the input as a polynomial, but over the Galois field GF(2). Instead of seeing the input as a polynomial of bytes, it is seen as a polynomial of bits, and all arithmetic is done in GF(2) (similarly to CRC-32). The hash is the remainder after the division of that polynomial by an irreducible polynomial over GF(2). It is possible to update a Rabin fingerprint using only the entering and the leaving byte, making it effectively a rolling hash.
Because it shares the same author as the Rabin–Karp string search algorithm, which is often explained with another, simpler rolling hash, and because this simpler rolling hash is also a polynomial, both rolling hashes are often mistaken for each other.


== Cyclic polynomial ==
Hashing by cyclic polynomial—sometimes called Buzhash—is also simple and it has the benefit of avoiding multiplications, using circular shift instead. It is a form of tabulation hashing: it presumes that there is some substitution function 
  
    
      
        s
      
    
    {\\displaystyle s}
  
 from characters to integers in the interval 
  
    
      
        [
        0
        ,
        
          2
          
            L
          
        
        )
      
    
    {\\displaystyle [0,2^{L})}
  
, essentially a lookup table (each of the 32 bit-positions of the values of s should be balanced, i.e. have as many 1s as there are 0s). Let the function 
  
    
      
        rol
      
    
    {\\displaystyle \\operatorname {rol} }
  
 be bitwise rotation. E.g., 
  
    
      
        rol
        ⁡
        (
        101
        )
        =
        011
      
    
    {\\displaystyle \\operatorname {rol} (101)=011}
  
. Let 
  
    
      
        ⊕
      
    
    {\\displaystyle \\oplus }
  
 be the bitwise exclusive or.""",
    tier=5,
    domain="computer_science",
    source="Wikipedia, 'Rolling hash'",
    source_url="https://en.wikipedia.org/wiki/Rolling_hash",
))

register_atom(Atom(
    atom_type="theorem",
    name="proof_by_induction",
    content="""Mathematical induction is a method for proving that a statement 
  
    
      
        P
        (
        n
        )
      
    
    {\\displaystyle P(n)}
  
 is true for every natural number 
  
    
      
        n
      
    
    {\\displaystyle n}
  
, that is, that the infinitely many cases 
  
    
      
        P
        (
        0
        )
        ,
        P
        (
        1
        )
        ,
        P
        (
        2
        )
        ,
        P
        (
        3
        )
        ,
        …
      
    
    {\\displaystyle P(0),P(1),P(2),P(3),\\dots }
  
  all hold. This is done by first proving a simple case, then also showing that if we assume the claim is true for a given case, then the next case is also true. Informal metaphors help to explain this technique, such as falling dominoes or climbing a ladder:

Mathematical induction proves that we can climb as high as we like on a ladder, by proving that we can climb onto the bottom rung (the basis) and that from each rung we can climb up to the next one (the step).
A proof by induction consists of two cases. The first, the base case, proves the statement for 
  
    
      
        n
        =
        0
      
    
    {\\displaystyle n=0}
  
 without assuming any knowledge of other cases. The second case, the induction step, proves that if the statement holds for any given case 
  
    
      
        n
        =
        k
      
    
    {\\displaystyle n=k}
  
, then it must also hold for the next case 
  
    
      
        n
        =
        k
        +
        1
      
    
    {\\displaystyle n=k+1}
  
. These two steps establish that the statement holds for every natural number 
  
    
      
        n
      
    
    {\\displaystyle n}
  
. The base case does not necessarily begin with 
  
    
      
        n
        =
        0
      
    
    {\\displaystyle n=0}
  
, but often with 
  
    
      
        n
        =
        1
      
    
    {\\displaystyle n=1}
  
, and possibly with any fixed natural number 
  
    
      
        n
        =
        N
      
    
    {\\displaystyle n=N}
  
, establishing the truth of the statement for all natural numbers 
  
    
      
        n
        ≥
        N
      
    
    {\\displaystyle n\\geq N}
  
.
The method can be extended to prove statements about more general well-founded structures, such as trees; this generalization, known as structural induction, is used in mathematical logic and computer science. Mathematical induction in this extended sense is closely related to recursion. Mathematical induction is an inference rule used in formal proofs, and is the foundation of most correctness proofs for computer programs.
Despite its name, mathematical induction differs fundamentally from inductive reasoning as used in philosophy, in which the examination of many cases results in a probable conclusion. The mathematical method examines infinitely many cases to prove a general statement, but it does so by a finite chain of deductive reasoning involving the variable 
  
    
      
        n
      
    
    {\\displaystyle n}
  
, which can take infinitely many values. The result is a rigorous proof of the statement, not an assertion of its probability.


== History ==
According to David E. Joyce, there is no evidence for the use of the principle of mathematical induction in Euclid’s writings. Acerbi (2000) argues that Plato’s Parmenides (c. 370 BC) contains traces of an early implicit inductive proof. This interpretation has been challenged by Negrepontis and Farmaki (2021), who further state that neither Plato nor any of the other Pythagoreans used the principle of mathematical induction.
The earliest implicit proof by mathematical induction was written by al-Karaji around 1000 AD, who applied it to arithmetic sequences to prove the binomial theorem and properties of Pascal's triangle. Whilst the original work was lost, it was later referenced by Al-Samawal al-Maghribi in his treatise al-Bahir fi'l-jabr (The Brilliant in Algebra) in around 1150 AD.

Katz says in his history of mathematics Another important idea introduced by al-Karaji and continued by al-Samaw'al and others was that of an inductive argument for dealing with certain arithmetic sequences. Thus al-Karaji used such an argument to prove the result on the sums of integral cubes already known to Aryabhata [...] Al-Karaji did not, however, state a general result for arbitrary n. He stated his theorem for the particular integer 10 [...] His proof, nevertheless, was clearly designed to be extendable to any other integer. [...] Al-Karaji's argument includes in essence the two basic components of a modern argument by induction, namely the truth of the statement for n = 1 (1 = 13) and the deriving of the truth for n = k from that of n = k − 1. Of course, this second component is not explicit since, in some sense, al-Karaji's argument is in reverse; this is, he starts from n = 10 and goes down to 1 rather than proceeding upward. Nevertheless, his argument in al-Fakhri is the earliest extant proof of the sum formula for integral cubes.
In India, early implicit proofs by mathematical induction appear in Bhaskara's "cyclic method".
None of these ancient mathematicians, however, explicitly stated the induction hypothesis. Another similar case (contrary to what Vacca has written, as Freudenthal carefully showed) was that of Francesco Maurolico in his Arithmeticorum libri duo (1575), who used the technique to prove that the sum of the first n odd integers is n2.
The earliest rigorous use of induction was by Gersonides (1288–1344). The first explicit formulation of the principle of induction was given by Pascal in his Traité du triangle arithmétique (1665). Another Frenchman, Fermat, made ample use of a related principle: indirect proof by infinite descent.
The induction hypothesis was also employed by the Swiss Jakob Bernoulli, and from then on it became well known. The modern formal treatment of the principle came only in the 19th century, with George Boole, Augustus De Morgan, Charles Sanders Peirce, Giuseppe Peano, and Richard Dedekind.


== Description ==
The simplest and most common form of mathematical induction infers that a statement involving a natural number n (that is, an integer n ≥ 0 or 1) holds for all values of n. The proof consists of two steps:

The base case (or initial case): prove that the statement holds for 0, or 1.
The induction step (or inductive step, or step case): prove that for every n, if the statement holds for n, then it holds for n + 1. In other words, assume that the statement holds for some arbitrary natural number n, and prove that the statement holds for n + 1.
The hypothesis in the induction step, that the statement holds for a particular n, is called the induction hypothesis or inductive hypothesis.""",
    tier=7,
    domain="logic",
    source="Wikipedia, 'Mathematical induction'",
    source_url="https://en.wikipedia.org/wiki/Mathematical_induction",
))

register_atom(Atom(
    atom_type="methodology",
    name="error_detection",
    content="""In mathematics, error analysis is the study of kind and quantity of error, or uncertainty, that may be present in the solution to a problem.  This issue is particularly prominent in applied areas such as numerical analysis and statistics.


== Error analysis in numerical modeling ==
In numerical simulation or modeling of real systems, error analysis is concerned with the changes in the output of the model as the parameters to the model vary about a mean.
For instance, in a system modeled as a function of two variables 
  
    
      
        z
        
        =
        
        f
        (
        x
        ,
        y
        )
        .
      
    
    {\\displaystyle z\\,=\\,f(x,y).}
  
  Error analysis deals with the propagation of the numerical errors in 
  
    
      
        x
      
    
    {\\displaystyle x}
  
 and 
  
    
      
        y
      
    
    {\\displaystyle y}
  
 (around mean values 
  
    
      
        
          
            
              x
              ¯
            
          
        
      
    
    {\\displaystyle {\\bar {x}}}
  
 and 
  
    
      
        
          
            
              y
              ¯
            
          
        
      
    
    {\\displaystyle {\\bar {y}}}
  
) to error in 
  
    
      
        z
      
    
    {\\displaystyle z}
  
 (around a mean 
  
    
      
        
          
            
              z
              ¯
            
          
        
      
    
    {\\displaystyle {\\bar {z}}}
  
).
In numerical analysis, error analysis comprises both forward error analysis and backward error analysis.


=== Forward error analysis ===
Forward error analysis involves the analysis of a function 
  
    
      
        
          z
          ′
        
        =
        
          f
          ′
        
        (
        
          a
          
            0
          
        
        ,
        
        
          a
          
            1
          
        
        ,
        
        …
        ,
        
        
          a
          
            n
          
        
        )
      
    
    {\\displaystyle z'=f'(a_{0},\\,a_{1},\\,\\dots ,\\,a_{n})}
  
 which is an approximation (usually a finite polynomial) to a function 
  
    
      
        z
        
        =
        
        f
        (
        
          a
          
            0
          
        
        ,
        
          a
          
            1
          
        
        ,
        …
        ,
        
          a
          
            n
          
        
        )
      
    
    {\\displaystyle z\\,=\\,f(a_{0},a_{1},\\dots ,a_{n})}
  
 to determine the bounds on the error in the approximation; i.e., to find 
  
    
      
        ϵ
      
    
    {\\displaystyle \\epsilon }
  
 such that 
  
    
      
        0
        
        ≤
        
        
          |
        
        z
        −
        
          z
          ′
        
        
          |
        
        
        ≤
        
        ϵ
        .
      
    
    {\\displaystyle 0\\,\\leq \\,|z-z'|\\,\\leq \\,\\epsilon .}
  
  The evaluation of forward errors is desired in validated numerics.


=== Backward error analysis ===
Backward error analysis involves the analysis of the approximation function 
  
    
      
        
          z
          ′
        
        
        =
        
        
          f
          ′
        
        (
        
          a
          
            0
          
        
        ,
        
        
          a
          
            1
          
        
        ,
        
        …
        ,
        
        
          a
          
            n
          
        
        )
        ,
      
    
    {\\displaystyle z'\\,=\\,f'(a_{0},\\,a_{1},\\,\\dots ,\\,a_{n}),}
  
 to determine the bounds on the parameters 
  
    
      
        
          a
          
            i
          
        
        
        =
        
        
          
            
              
                a
                
                  i
                
              
              ¯
            
          
        
        
        ±
        
        
          ϵ
          
            i
          
        
      
    
    {\\displaystyle a_{i}\\,=\\,{\\bar {a_{i}}}\\,\\pm \\,\\epsilon _{i}}
  
 such that the result 
  
    
      
        
          z
          ′
        
        
        =
        
        z
        .
      
    
    {\\displaystyle z'\\,=\\,z.}
  

Backward error analysis, the theory of which was developed and popularized by James H. Wilkinson, can be used to establish that an algorithm implementing a numerical function is numerically stable. The basic approach is to show that although the calculated result, due to roundoff errors, will not be exactly correct, it is the exact solution to a nearby problem with slightly perturbed input data. If the perturbation required is small, on the order of the uncertainty in the input data, then the results are in some sense as accurate as the data "deserves". The algorithm is then defined as backward stable. Stability is a measure of the sensitivity to rounding errors of a given numerical procedure;  by contrast, the condition number of a function for a given problem indicates the inherent sensitivity of the function to small perturbations in its input and is independent of the implementation used to solve the problem.


== Applications ==


=== Global positioning system ===

The analysis of errors computed using the global positioning system is important for understanding how GPS works, and for knowing what magnitude errors should be expected. The Global Positioning System makes corrections for receiver clock errors and other effects but there are still residual errors which are not corrected. The Global Positioning System (GPS) was created by the United States Department of Defense (DOD) in the 1970s. It has come to be widely used for navigation both by the U.S. military and the general public.


=== Molecular dynamics simulation ===
In molecular dynamics (MD) simulations, there are errors due to inadequate sampling of the phase space or infrequently occurring events, these lead to the statistical error due to random fluctuation in the measurements.
For a series of M measurements of a fluctuating property A, the mean value is:

  
    
      
        ⟨
        A
        ⟩
        =
        
          
            1
            M
          
        
        
          ∑
          
            μ
            =
            1
          
          
            M
          
        
        
          A
          
            μ
          
        
        .
      
    
    {\\displaystyle \\langle A\\rangle ={\\frac {1}{M}}\\sum _{\\mu =1}^{M}A_{\\mu }.}
  

When these M measurements are independent, the variance of the mean ⟨A⟩ is:

  
    
      
        
          σ
          
            2
          
        
        (
        ⟨
        A
        ⟩
        )
        =
        
          
            1
            M
          
        
        
          σ
          
            2
          
        
        (
        A
        )
        ,
      
    
    {\\displaystyle \\sigma ^{2}(\\langle A\\rangle )={\\frac {1}{M}}\\sigma ^{2}(A),}
  

but in most MD simulations, there is correlation between quantity A at different time, so the variance of the mean ⟨A⟩ will be underestimated as the effective number of independent measurements is actually less than M.""",
    tier=7,
    domain="methodology",
    source="Wikipedia, 'Error analysis (mathematics)'",
    source_url="https://en.wikipedia.org/wiki/Error_analysis_%28mathematics%29",
))

register_atom(Atom(
    atom_type="principle",
    name="algorithm_design",
    content="""In mathematics and computer science, an algorithm ( ) is a finite sequence of mathematically rigorous instructions, typically used to solve a class of specific problems or to perform a computation. Algorithms are used as specifications for performing calculations and data processing. More advanced algorithms can use conditionals to divert the code execution through various routes (referred to as automated decision-making) and deduce valid inferences (referred to as automated reasoning).
In contrast, a heuristic is an approach to solving problems without well-defined correct or optimal results. For example, although social media recommender systems are commonly called \"algorithms\", they actually rely on heuristics as there is no truly \"correct\" recommendation.
As an effective method, an algorithm can be expressed within a finite amount of space and time and in a well-defined formal language for calculating a function. Starting from an initial state and input, a computation occurs at each step, eventually producing output and terminating. The transition between states can be non-deterministic; randomized algorithms incorporate random input.

""",
    tier=9,
    domain="computer_science",
    source="Wikipedia, 'Algorithm'",
    source_url="https://en.wikipedia.org/wiki/Algorithm",
))

register_atom(Atom(
    atom_type="theorem",
    name="gradient_analysis",
    content="""In machine learning, backpropagation is a gradient computation method commonly used for training a neural network in computing parameter updates.
It is an efficient application of the chain rule to neural networks. Backpropagation efficiently computes the gradient of the loss with respect to the network weights for a single input–output example. It does this by propagating derivatives backward, one layer at a time, from the output layer to the input layer, thereby avoiding redundant chain-rule calculations.
Strictly speaking, the term backpropagation refers only to an algorithm for efficiently computing the gradient, not how the gradient is used, but the term is often used loosely to refer to the entire learning algorithm. This includes changing model parameters in the negative direction of the gradient, such as by stochastic gradient descent, or as an intermediate step in a more complicated optimizer, such as Adaptive Moment Estimation.
Backpropagation had multiple discoveries and partial discoveries, with a tangled history and terminology (see § History). Some other names for the technique include "reverse mode of automatic differentiation" or "reverse accumulation".


== Overview ==
Backpropagation computes the gradient in weight space of a feedforward neural network, with respect to a loss function. Denote:

  
    
      
        x
      
    
    {\\displaystyle x}
  
: input (vector of features)

  
    
      
        y
      
    
    {\\displaystyle y}
  
: target output
For classification, output will be a vector of class probabilities (e.g., 
  
    
      
        (
        0.1
        ,
        0.7
        ,
        0.2
        )
      
    
    {\\displaystyle (0.1,0.7,0.2)}
  
, and target output is a specific class, encoded by the one-hot/dummy variable (e.g., 
  
    
      
        (
        0
        ,
        1
        ,
        0
        )
      
    
    {\\displaystyle (0,1,0)}
  
).

  
    
      
        C
      
    
    {\\displaystyle C}
  
: loss function or "cost function"
For classification, this is usually cross-entropy (XC, log loss), while for regression it is usually squared error loss (SEL).

  
    
      
        L
      
    
    {\\displaystyle L}
  
: the number of layers

  
    
      
        
          W
          
            l
          
        
        =
        (
        
          w
          
            j
            k
          
          
            l
          
        
        )
      
    
    {\\displaystyle W^{l}=(w_{jk}^{l})}
  
: the weights between layer 
  
    
      
        l
        −
        1
      
    
    {\\displaystyle l-1}
  
 and 
  
    
      
        l
      
    
    {\\displaystyle l}
  
, where 
  
    
      
        
          w
          
            j
            k
          
          
            l
          
        
      
    
    {\\displaystyle w_{jk}^{l}}
  
 is the weight between the 
  
    
      
        k
      
    
    {\\displaystyle k}
  
-th node in layer 
  
    
      
        l
        −
        1
      
    
    {\\displaystyle l-1}
  
 and the 
  
    
      
        j
      
    
    {\\displaystyle j}
  
-th node in layer 
  
    
      
        l
      
    
    {\\displaystyle l}
  

  
    
      
        
          f
          
            l
          
        
      
    
    {\\displaystyle f^{l}}
  
: activation functions at layer 
  
    
      
        l
      
    
    {\\displaystyle l}
  

For classification the last layer is usually the logistic function for binary classification, and softmax (softargmax) for multi-class classification, while for the hidden layers this was traditionally a sigmoid function (logistic function or others) on each node (coordinate), but today is more varied, with rectifier (ramp, ReLU) being common.

  
    
      
        
          a
          
            j
          
          
            l
          
        
      
    
    {\\displaystyle a_{j}^{l}}
  
: activation of the 
  
    
      
        j
      
    
    {\\displaystyle j}
  
-th node in layer 
  
    
      
        l
      
    
    {\\displaystyle l}
  
.
In the derivation of backpropagation, other intermediate quantities are used by introducing them as needed below. Bias terms are not treated specially since they correspond to a weight with a fixed input of 1. For backpropagation the specific loss function and activation functions do not matter as long as they and their derivatives can be evaluated efficiently. Traditional activation functions include sigmoid, tanh, ReLU, Swish, Mish,, and many others.
The overall network is a combination of function composition and matrix multiplication:

  
    
      
        g
        (
        x
        )
        :=
        
          f
          
            L
          
        
        (
        
          W
          
            L
          
        
        
          f
          
            L
            −
            1
          
        
        (
        
          W
          
            L
            −
            1
          
        
        ⋯
        
          f
          
            1
          
        
        (
        
          W
          
            1
          
        
        x
        )
        ⋯
        )
        )
      
    
    {\\displaystyle g(x):=f^{L}(W^{L}f^{L-1}(W^{L-1}\\cdots f^{1}(W^{1}x)\\cdots ))}
  

For a training set there will be a set of input–output pairs, 
  
    
      
        
          {
          
            (
            
              x
              
                i
              
            
            ,
            
              y
              
                i
              
            
            )
          
          }
        
      
    
    {\\displaystyle \\left\\{(x_{i},y_{i})\\right\\}}
  
. For each input–output pair 
  
    
      
        (
        
          x
          
            i
          
        
        ,
        
          y
          
            i
          
        
        )
      
    
    {\\displaystyle (x_{i},y_{i})}
  
 in the training set, the loss of the model on that pair is the cost of the difference between the predicted output 
  
    
      
        g
        (
        
          x
          
            i
          
        
        )
      
    
    {\\displaystyle g(x_{i})}
  
 and the target output 
  
    
      
        
          y
          
            i
          
        
      
    
    {\\displaystyle y_{i}}
  
:

  
    
      
        C
        (
        
          y
          
            i
          
        
        ,
        g
        (
        
          x
          
            i
          
        
        )
        )
      
    
    {\\displaystyle C(y_{i},g(x_{i}))}
  

Note the distinction: during model evaluation the weights are fixed while the inputs vary (and the target output may be unknown), and the network ends with the output layer (it does not include the loss function). During model training the input–output pair is fixed while the weights vary, and the network ends with the loss function.
Backpropagation computes the gradient for a fixed input–output pair 
  
    
      
        (
        
          x
          
            i
          
        
        ,
        
          y
          
            i
          
        
        )
      
    
    {\\displaystyle (x_{i},y_{i})}
  
, where the weights 
  
    
      
        
          w
          
            j
            k
          
          
            l
          
        
      
    
    {\\displaystyle w_{jk}^{l}}
  
 can vary.""",
    tier=10,
    domain="deep_learning",
    source="Wikipedia, 'Backpropagation'",
    source_url="https://en.wikipedia.org/wiki/Backpropagation",
))

register_atom(Atom(
    atom_type="result",
    name="scaling_prediction",
    content="""In machine learning, a neural scaling law is an empirical scaling law that describes how neural network performance changes as key factors are scaled up or down. These factors typically include the number of parameters, training dataset size, and training cost. Some models also exhibit performance gains by scaling inference through increased test-time compute (TTC), extending neural scaling laws beyond training to the deployment phase.


== Introduction ==
In general, a deep learning model can be characterized by four parameters: model size, training dataset size, training cost, and the post-training error rate (e.g., the test set error rate). Each of these variables can be defined as a real number, usually written as 
  
    
      
        N
        ,
        D
        ,
        C
        ,
        L
      
    
    {\\displaystyle N,D,C,L}
  
 (respectively: parameter count, dataset size, computing cost, and loss).
A neural scaling law is a theoretical or empirical statistical law between these parameters. There are also other parameters with other scaling laws.


=== Size of the model ===
In most cases, the model's size is simply the number of parameters. However, one complication arises with the use of sparse models, such as mixture-of-expert models. With sparse models, during inference, only a fraction of their parameters are used. In comparison, most other kinds of neural networks, such as transformer models, always use all their parameters during inference.


=== Size of the training dataset ===
The size of the training dataset is usually quantified by the number of data points within it. Larger training datasets are typically preferred, as they provide a richer and more diverse source of information from which the model can learn. This can lead to improved generalization performance when the model is applied to new, unseen data. However, increasing the size of the training dataset also increases the computational resources and time required for model training.
With the "pretrain, then finetune" method used for most large language models, there are two kinds of training dataset: the pretraining dataset and the finetuning dataset. Their sizes have different effects on model performance. Generally, the finetuning dataset is less than 1% the size of pretraining dataset.
In some cases, a small amount of high quality data suffices for finetuning, and more data does not necessarily improve performance.


=== Cost of training ===

Training cost is typically measured in terms of time (how long it takes to train the model) and computational resources (how much processing power and memory are required). It is important to note that the cost of training can be significantly reduced with efficient training algorithms, optimized software libraries, and parallel computing on specialized hardware such as GPUs or TPUs.
The cost of training a neural network model is a function of several factors, including model size, training dataset size, the training algorithm complexity, and the computational resources available. In particular, doubling the training dataset size does not necessarily double the cost of training, because one may train the model for several times over the same dataset (each being an "epoch").


=== Performance ===

The performance of a neural network model is evaluated based on its ability to accurately predict the output given some input data. Common metrics for evaluating model performance include:

Negative log-likelihood per token (logarithm of perplexity) for language modeling;
Accuracy, precision, recall, and F1 score for classification tasks;
Mean squared error (MSE) or mean absolute error (MAE) for regression tasks;
Elo rating in a competition against other models, such as gameplay or preference by a human judge.
Performance can be improved by using more data, larger models, different training algorithms, regularizing the model to prevent overfitting, and early stopping using a validation set.
When the performance is a number bounded within the range of 
  
    
      
        [
        0
        ,
        1
        ]
      
    
    {\\displaystyle [0,1]}
  
, such as accuracy, precision, etc., it often scales as a sigmoid function of cost, as seen in the figures.


== Examples ==


=== (Hestness, Narang, et al, 2017) ===
The 2017 paper is a common reference point for neural scaling laws fitted by statistical analysis on experimental data. Previous works before the 2000s, as cited in the paper, were either theoretical or orders of magnitude smaller in scale. Whereas previous works generally found the scaling exponent to scale like 
  
    
      
        L
        ∝
        
          D
          
            −
            α
          
        
      
    
    {\\displaystyle L\\propto D^{-\\alpha }}
  
, with 
  
    
      
        α
        ∈
        {
        0.5
        ,
        1
        ,
        2
        }
      
    
    {\\displaystyle \\alpha \\in \\{0.5,1,2\\}}
  
, the paper found that 
  
    
      
        α
        ∈
        [
        0.07
        ,
        0.35
        ]
      
    
    {\\displaystyle \\alpha \\in [0.07,0.35]}
  
.
Of the factors they varied, only task can change the exponent 
  
    
      
        α
      
    
    {\\displaystyle \\alpha }
  
. Changing the architecture optimizers, regularizers, and loss functions, would only change the proportionality factor, not the exponent. For example, for the same task, one architecture might have 
  
    
      
        L
        =
        1000
        
          D
          
            −
            0.3
          
        
      
    
    {\\displaystyle L=1000D^{-0.3}}
  
 while another might have 
  
    
      
        L
        =
        500
        
          D
          
            −
            0.3
          
        
      
    
    {\\displaystyle L=500D^{-0.3}}
  
.""",
    tier=10,
    domain="deep_learning",
    source="Wikipedia, 'Neural scaling law'",
    source_url="https://en.wikipedia.org/wiki/Neural_scaling_law",
))

register_atom(Atom(
    atom_type="principle",
    name="constraint_optimisation",
    content="""In mathematical optimization, constrained optimization (in some contexts called constraint optimization) is the process of optimizing an objective function with respect to some variables  in the presence of constraints on those variables. The objective function is either a cost function or energy function, which is to be minimized, or a reward function or utility function, which is to be maximized. Constraints can be either hard constraints, which set conditions for the variables that are required to be satisfied, or soft constraints, which have some variable values that are penalized in the objective function if, and based on the extent that, the conditions on the variables are not satisfied.


== Relation to constraint-satisfaction problems ==
The constrained-optimization problem (COP) is a significant generalization of the classic constraint-satisfaction problem (CSP) model. COP is a CSP that includes an objective function to be optimized.  Many algorithms are used to handle the optimization part.


== General form ==
A general constrained minimization problem may be written as follows:

  
    
      
        
          
            
              
                min
              
              
                 
              
              
                f
                (
                
                  x
                
                )
              
              
            
            
              
                
                  s
                  u
                  b
                  j
                  e
                  c
                  t
                   
                  t
                  o
                
              
              
                 
              
              
                
                  g
                  
                    i
                  
                
                (
                
                  x
                
                )
                =
                
                  c
                  
                    i
                  
                
              
              
                
                  for 
                
                i
                =
                1
                ,
                …
                ,
                n
                
                
                  Equality constraints
                
              
            
            
              
              
                 
              
              
                
                  h
                  
                    j
                  
                
                (
                
                  x
                
                )
                ≥
                
                  d
                  
                    j
                  
                
              
              
                
                  for 
                
                j
                =
                1
                ,
                …
                ,
                m
                
                
                  Inequality constraints
                
              
            
          
        
      
    
    {\\displaystyle {\\begin{array}{rcll}\\min &~&f(\\mathbf {x} )&\\\\\\mathrm {subject~to} &~&g_{i}(\\mathbf {x} )=c_{i}&{\\text{for }}i=1,\\ldots ,n\\quad {\\text{Equality constraints}}\\\\&~&h_{j}(\\mathbf {x} )\\geq d_{j}&{\\text{for }}j=1,\\ldots ,m\\quad {\\text{Inequality constraints}}\\end{array}}}
  

where 
  
    
      
        
          g
          
            i
          
        
        (
        
          x
        
        )
        =
        
          c
          
            i
          
        
         
        
          f
          o
          r
           
        
        i
        =
        1
        ,
        …
        ,
        n
      
    
    {\\displaystyle g_{i}(\\mathbf {x} )=c_{i}~\\mathrm {for~} i=1,\\ldots ,n}
  
 and 
  
    
      
        
          h
          
            j
          
        
        (
        
          x
        
        )
        ≥
        
          d
          
            j
          
        
         
        
          f
          o
          r
           
        
        j
        =
        1
        ,
        …
        ,
        m
      
    
    {\\displaystyle h_{j}(\\mathbf {x} )\\geq d_{j}~\\mathrm {for~} j=1,\\ldots ,m}
  
 are constraints that are required to be satisfied (these are called hard constraints), and 
  
    
      
        f
        (
        
          x
        
        )
      
    
    {\\displaystyle f(\\mathbf {x} )}
  
 is the objective function that needs to be optimized subject to the constraints.
In some problems, often called constraint optimization problems, the objective function is actually the sum of cost functions, each of which penalizes the extent (if any) to which a soft constraint (a constraint which is preferred but not required to be satisfied) is violated.


== Solution methods ==
Many unconstrained optimization algorithms can be adapted to the constrained case, often via the use of a penalty method. However, search steps taken by the unconstrained method may be unacceptable for the constrained problem, leading to a lack of convergence. This is referred to as the Maratos effect.


=== Equality constraints ===


==== Substitution method ====
For very simple problems, say a function of two variables subject to a single equality constraint, it is most practical to apply the method of substitution. The idea is to substitute the constraint into the objective function to create a composite function that incorporates the effect of the constraint. For example, assume the objective is to maximize 
  
    
      
        f
        (
        x
        ,
        y
        )
        =
        x
        ⋅
        y
      
    
    {\\displaystyle f(x,y)=x\\cdot y}
  
 subject to 
  
    
      
        x
        +
        y
        =
        10
      
    
    {\\displaystyle x+y=10}
  
. The constraint implies 
  
    
      
        y
        =
        10
        −
        x
      
    
    {\\displaystyle y=10-x}
  
, which can be substituted into the objective function to create 
  
    
      
        p
        (
        x
        )
        =
        x
        (
        10
        −
        x
        )
        =
        10
        x
        −
        
          x
          
            2
          
        
      
    
    {\\displaystyle p(x)=x(10-x)=10x-x^{2}}
  
. The first-order necessary condition gives 
  
    
      
        
          
            
              ∂
              p
            
            
              ∂
              x
            
          
        
        =
        10
        −
        2
        x
        =
        0
      
    
    {\\displaystyle {\\frac {\\partial p}{\\partial x}}=10-2x=0}
  
, which can be solved for 
  
    
      
        x
        =
        5
      
    
    {\\displaystyle x=5}
  
 and, consequently, 
  
    
      
        y
        =
        10
        −
        5
        =
        5
      
    
    {\\displaystyle y=10-5=5}
  
.


==== Lagrange multiplier ====

If the constrained problem has only equality constraints, the method of Lagrange multipliers can be used to convert it into an unconstrained problem whose number of variables is the original number of variables plus the original number of equality constraints.""",
    tier=7,
    domain="optimisation",
    source="Wikipedia, 'Constrained optimization'",
    source_url="https://en.wikipedia.org/wiki/Constrained_optimization",
))

register_atom(Atom(
    atom_type="methodology",
    name="problem_construction",
    content="""Problem solving is the process of achieving a goal by overcoming obstacles, a frequent part of most activities. Problems in need of solutions range from simple personal tasks (e.g. how to turn on an appliance) to complex issues in business and technical fields. The former is an example of simple problem solving (SPS) addressing one issue, whereas the latter is complex problem solving (CPS) with multiple interrelated obstacles. Another classification of problem-solving tasks is into well-defined problems with specific obstacles and goals, and ill-defined problems in which the current situation is troublesome but it is not clear what kind of resolution to aim for. Similarly, one may distinguish formal or fact-based problems requiring psychometric intelligence, versus socio-emotional problems which depend on the changeable emotions of individuals or groups, such as tactful behavior, fashion, or gift choices.
Solutions require sufficient resources and knowledge to attain the goal. Professionals such as lawyers, doctors, programmers, and consultants are largely problem solvers for issues that require technical skills and knowledge beyond general competence. Many businesses have found profitable markets by recognizing a problem and creating a solution: the more widespread and inconvenient the problem, the greater the opportunity to develop a scalable solution.
There are many specialized problem-solving techniques and methods in fields such as science, engineering, business, medicine, mathematics, computer science, philosophy, and social organization. The mental techniques to identify, analyze, and solve problems are studied in psychology and cognitive sciences. Also widely researched are the mental obstacles that prevent people from finding solutions; problem-solving impediments include confirmation bias, mental set, and functional fixedness.


== Definition ==
The term problem solving has a slightly different meaning depending on the discipline. For instance, it is a mental process in psychology and a computerized process in computer science. There are two different types of problems: ill-defined and well-defined; different approaches are used for each. Well-defined problems have specific end goals and clearly expected solutions, while ill-defined problems do not. Well-defined problems allow for more initial planning than ill-defined problems. Solving problems sometimes involves dealing with pragmatics (the way that context contributes to meaning) and semantics (the interpretation of the problem). The ability to understand what the end goal of the problem is, and what rules could be applied, represents the key to solving the problem. Sometimes a problem requires abstract thinking or coming up with a creative solution.
Problem solving has two major domains: mathematical problem solving and personal problem solving. Each concerns some difficulty or barrier that is encountered.


=== Psychology ===
Problem solving in psychology refers to the process of finding solutions to problems encountered in life. Solutions to these problems are usually situation- or context-specific. The process starts with problem finding and problem shaping, in which the problem is discovered and simplified. The next step is to generate possible solutions and evaluate them. Finally a solution is selected to be implemented and verified. Problems have an end goal to be reached; how you get there depends upon problem orientation (problem-solving coping style and skills) and systematic analysis.
Mental health professionals study the human problem-solving processes using methods such as introspection, behaviorism, simulation, computer modeling, and experiment. Social psychologists look into the person-environment relationship aspect of the problem and independent and interdependent problem-solving methods. Problem solving has been defined as a higher-order cognitive process and intellectual function that requires the modulation and control of more routine or fundamental skills.
Empirical research shows many different strategies and factors influence everyday problem solving. Rehabilitation psychologists studying people with frontal lobe injuries have found that deficits in emotional control and reasoning can be re-mediated with effective rehabilitation and could improve the capacity of injured persons to resolve everyday problems. Interpersonal everyday problem solving is dependent upon personal motivational and contextual components. One such component is the emotional valence of "real-world" problems, which can either impede or aid problem-solving performance. Researchers have focused on the role of emotions in problem solving, demonstrating that poor emotional control can disrupt focus on the target task, impede problem resolution, and lead to negative outcomes such as fatigue, depression, and inertia. In conceptualization,human problem solving consists of two related processes: problem orientation, and the motivational/attitudinal/affective approach to problematic situations and problem-solving skills. People's strategies cohere with their goals and stem from the process of comparing oneself with others.


=== Cognitive sciences ===
Among the first experimental psychologists to study problem solving were the Gestaltists in Germany, such as Karl Duncker in The Psychology of Productive Thinking (1935). Perhaps best known is the work of Allen Newell and Herbert A. Simon.
Experiments in the 1960s and early 1970s asked participants to solve relatively simple, well-defined, but not previously seen laboratory tasks. These simple problems, such as the Tower of Hanoi, admitted optimal solutions that could be found quickly, allowing researchers to observe the full problem-solving process. Researchers assumed that these model problems would elicit the characteristic cognitive processes by which more complex "real world" problems are solved.
An outstanding problem-solving technique found by this research is the principle of decomposition.


=== Computer science ===

Much of computer science and artificial intelligence involves designing automated systems to solve a specified type of problem: to accept input data and calculate a correct or adequate response, reasonably quickly. Algorithms are recipes or instructions that direct such systems, written into computer programs.
Steps for designing such systems include problem determination, heuristics, root cause analysis, de-duplication, analysis, diagnosis, and repair. Analytic techniques include linear and nonlinear programming, queuing systems, and simulation. A large, perennial obstacle is to find and fix errors in computer programs: debugging.


=== Logic ===
Formal logic concerns issues like validity, truth, inference, argumentation, and proof. In a problem-solving context, it can be used to formally represent a problem as a theorem to be proved, and to represent the knowledge needed to solve the problem as the premises to be used in a proof that the problem has a solution.
The use of computers to prove mathematical theorems using formal logic emerged as the field of automated theorem proving in the 1950s. It included the use of heuristic methods designed to simulate human problem solving, as in the Logic Theory Machine, developed by Allen Newell, Herbert A. Simon and J. C. Shaw, as well as algorithmic methods such as the resolution principle developed by John Alan Robinson.
In addition to its use for finding proofs of mathematical theorems, automated theorem-proving has also been used for program verification in computer science. In 1958, John McCarthy proposed the advice taker, to represent information in formal logic and to derive answers to questions using automated theorem-proving.""",
    tier=7,
    domain="methodology",
    source="Wikipedia, 'Problem solving'",
    source_url="https://en.wikipedia.org/wiki/Problem_solving",
))

register_atom(Atom(
    atom_type="principle",
    name="complexity_analysis",
    content="""In theoretical computer science and mathematics, computational complexity theory focuses on classifying computational problems according to their resource usage, and explores the relationships between these classifications. A computational problem is a task solved by a computer and is solvable by mechanical application of mathematical steps, such as an algorithm.
A problem is regarded as inherently difficult if its solution requires significant resources, whatever the algorithm used. The theory formalizes this intuition, by introducing mathematical models of computation to study these problems and quantifying their computational complexity, i.e., the amount of resources needed to solve them, such as time and storage. 
Other measures of complexity are also used, such as the amount of communication (used in communication complexity), the number of gates in a circuit (used in circuit complexity) and the number of processors (used in parallel computing). One of the roles of computational complexity theory is to determine the practical limits on what computers can and cannot do. The P versus NP problem, one of the seven Millennium Prize Problems, is part of the field of computational complexity.
Closely related fields in theoretical computer science are analysis of algorithms and computability theory. A key distinction between analysis of algorithms and computational complexity theory is that the former is devoted to analyzing the amount of resources needed by a particular algorithm to solve a problem, whereas the latter asks a more general question about all possible algorithms that could be used to solve the same problem. More precisely, computational complexity theory tries to classify problems that can or cannot be solved with appropriately restricted resources. In turn, imposing restrictions on the available resources is what distinguishes computational complexity from computability theory: the latter theory asks what kinds of problems can, in principle, be solved algorithmically.


== Computational problems ==


=== Problem instances ===
A computational problem can be viewed as an infinite collection of instances together with a set (possibly empty) of solutions for every instance. The input string for a computational problem is referred to as a problem instance, and should not be confused with the problem itself. In computational complexity theory, a problem refers to the abstract question to be solved. In contrast, an instance of this problem is a rather concrete utterance, which can serve as the input for a decision problem. For example, consider the problem of primality testing. The instance is a number (e.g., 15) and the solution is "yes" if the number is prime and "no" otherwise (in this case, 15 is not prime and the answer is "no"). Stated another way, the instance is a particular input to the problem, and the solution is the output corresponding to the given input.
To further highlight the difference between a problem and an instance, consider the following instance of the decision version of the travelling salesman problem: Is there a route of at most 2000 kilometres passing through all of Germany's 14 largest cities? The quantitative answer to this particular problem instance is of little use for solving other instances of the problem, such as asking for a round trip through 14 sites in Milan whose total length is at most 10 km. For this reason, complexity theory addresses computational problems and not particular problem instances.


=== Representing problem instances ===
When considering computational problems, a problem instance is a string over an alphabet. Usually, the alphabet is taken to be the binary alphabet (i.e., the set {0,1}), and thus the strings are bitstrings. As in a real-world computer, mathematical objects other than bitstrings must be suitably encoded. For example, integers can be represented in binary notation, and graphs can be encoded directly via their adjacency matrices, or by encoding their adjacency lists in binary.
Even though some proofs of complexity-theoretic theorems regularly assume some concrete choice of input encoding, one tries to keep the discussion abstract enough to be independent of the precise choice of encoding. This can be achieved by ensuring that different representations can be transformed into each other efficiently.


=== Decision problems as formal languages ===

Decision problems are one of the central objects of study in computational complexity theory. A decision problem is a type of computational problem where the answer is either yes or no (alternatively, 1 or 0). A decision problem can be viewed as a formal language, where the members of the language are instances whose output is yes, and the non-members are those instances whose output is no. The objective is to decide, with the aid of an algorithm, whether a given input string is a member of the formal language under consideration. If the algorithm deciding this problem returns the answer yes, the algorithm is said to accept the input string, otherwise it is said to reject the input.
An example of a decision problem is the following. The input is an arbitrary graph. The problem consists in deciding whether the given graph is connected or not. The formal language associated with this decision problem is then the set of all connected graphs—to obtain a precise definition of this language, one has to decide how graphs are encoded as binary strings.


=== Function problems ===
A function problem is a computational problem where a single output (of a total function) is expected for every input, but the output can be more complex than that of a decision problem—that is, the output is not just yes or no. Notable examples include the traveling salesman problem and the integer factorization problem.
It is tempting to think that the notion of function problems is much richer than the notion of decision problems. However, this is not really the case, since function problems can be recast as decision problems. For example, the multiplication of two integers can be expressed as the set of triples 
  
    
      
        (
        a
        ,
        b
        ,
        c
        )
      
    
    {\\displaystyle (a,b,c)}
  
 such that the relation 
  
    
      
        a
        ×
        b
        =
        c
      
    
    {\\displaystyle a\\times b=c}
  
 holds. Deciding whether a given triple is a member of this set corresponds to solving the problem of multiplying two numbers.


=== Measuring the size of an instance ===
To measure the difficulty of solving a computational problem, one may wish to see how much time the best algorithm requires to solve the problem. However, the running time may, in general, depend on the instance. In particular, larger instances will require more time to solve. Thus the time required to solve a problem (or the space required, or any measure of complexity) is calculated as a function of the size of the instance. The input size is typically measured in bits. Complexity theory studies how algorithms scale as input size increases. For instance, in the problem of finding whether a graph is connected, how much more time does it take to solve a problem for a graph with 
  
    
      
        2
        n
      
    
    {\\displaystyle 2n}
  
 vertices compared to the time taken for a graph with 
  
    
      
        n
      
    
    {\\displaystyle n}
  
 vertices?
If the input size is 
  
    
      
        n
      
    
    {\\displaystyle n}
  
, the time taken can be expressed as a function of 
  
    
      
        n
      
    
    {\\displaystyle n}
  
. Since the time taken on different inputs of the same size can be different, the worst-case time complexity 
  
    
      
        T
        (
        n
        )
      
    
    {\\displaystyle T(n)}
  
 is defined to be the maximum time taken over all inputs of size 
  
    
      
        n
      
    
    {\\displaystyle n}
  
.""",
    tier=7,
    domain="computer_science",
    source="Wikipedia, 'Computational complexity theory'",
    source_url="https://en.wikipedia.org/wiki/Computational_complexity_theory",
))

register_atom(Atom(
    atom_type="methodology",
    name="error_correction",
    content="""In information theory and coding theory with applications in computer science and telecommunications, error detection and correction (EDAC) or error control are techniques that enable reliable delivery of digital data over unreliable communication channels. Many communication channels are subject to channel noise, and thus errors may be introduced during transmission from the source to a receiver. Error detection techniques allow detecting such errors, while error correction enables reconstruction of the original data in many cases.


== Definitions ==
Error detection is the detection of errors caused by noise or other impairments during transmission from the transmitter to the receiver.
Error correction is the detection of errors and reconstruction of the original, error-free data.


== History ==
In classical antiquity, copyists of the Hebrew Bible were paid for their work according to the number of stichs (lines of verse). As the prose books of the Bible were hardly ever written in stichs, the copyists, in order to estimate the amount of work, had to count the letters. This also helped ensure accuracy in the transmission of the text with the production of subsequent copies. Between the 7th and 10th centuries CE a group of Jewish scribes formalized and expanded this to create the Numerical Masorah to ensure accurate reproduction of the sacred text. It included counts of the number of words in a line, section, book and groups of books, noting the middle stich of a book, word use statistics, and commentary. Standards became such that a deviation in even a single letter in a Torah scroll was considered unacceptable. The effectiveness of their error correction method was verified by the accuracy of copying through the centuries demonstrated by discovery of the Dead Sea Scrolls in 1947–1956, dating from c. 150 BCE – 75 CE.
The modern development of error correction codes is credited to Richard Hamming in 1947. A description of Hamming's code appeared in Claude Shannon's A Mathematical Theory of Communication and was quickly generalized by Marcel J. E. Golay.


== Principles ==
All error-detection and correction schemes add some redundancy (i.e., some extra data) to a message, which receivers can use to check consistency of the delivered message and to recover data that has been determined to be corrupted. Error detection and correction schemes can be either systematic or non-systematic. In a systematic scheme, the transmitter sends the original (error-free) data and attaches a fixed number of check bits (or parity data), which are derived from the data bits by some encoding algorithm. If error detection is required, a receiver can simply apply the same algorithm to the received data bits and compare its output with the received check bits; if the values do not match, an error has occurred at some point during the transmission. If error correction is required, a receiver can apply the decoding algorithm to the received data bits and the received check bits to recover the original error-free data. In a system that uses a non-systematic code, the original message is transformed into an encoded message carrying the same information, and that has at least as many bits as the original message.
Good error control performance requires the scheme to be selected based on the characteristics of the communication channel. Common channel models include memoryless models where errors occur randomly and with a certain probability, and dynamic models where errors occur primarily in bursts. Consequently, error-detecting and -correcting codes can be generally distinguished between random-error-detecting/correcting and burst-error-detecting/correcting. Some codes can also be suitable for a mixture of random errors and burst errors.
If the channel characteristics cannot be determined or are highly variable, an error-detection scheme may be combined with a system for retransmission of erroneous data. This is known as automatic repeat request (ARQ), and is most notably used on the Internet. An alternate approach for error control is hybrid automatic repeat request (HARQ), which is a combination of ARQ and error-correction coding.


== Types of error correction ==
There are three major types of error correction:


=== Automatic repeat request ===
Automatic repeat request (ARQ) is an error control method for data transmission that makes use of error-detection codes, acknowledgment and/or negative acknowledgment messages, and timeouts to achieve reliable data transmission. An acknowledgment is a message sent by the receiver to indicate that it has correctly received a data frame.
Usually, when the transmitter does not receive the acknowledgment before the timeout occurs (i.e., within a reasonable amount of time after sending the data frame), it retransmits the frame until it is either correctly received or the error persists beyond a predetermined number of retransmissions.
Three types of ARQ protocols are Stop-and-wait ARQ, Go-Back-N ARQ, and Selective Repeat ARQ.
ARQ is appropriate if the communication channel has varying or unknown capacity, such as is the case on the Internet. However, ARQ requires the availability of a back channel, results in possibly increased latency due to retransmissions, and requires the maintenance of buffers and timers for retransmissions, which in the case of network congestion can put a strain on the server and overall network capacity.
For example, ARQ is used on shortwave radio data links in the form of ARQ-E, or combined with multiplexing as ARQ-M.


=== Forward error correction ===
Forward error correction (FEC) is a process of adding redundant data such as an error-correcting code (ECC) to a message so that it can be recovered by a receiver even when a number of errors (up to the capability of the code being used) are introduced, either during the process of transmission or on storage. Since the receiver does not have to ask the sender for retransmission of the data, a backchannel is not required in forward error correction. Error-correcting codes are used in lower-layer communication such as cellular network, high-speed fiber-optic communication and Wi-Fi, as well as for reliable storage in media such as flash memory, hard disk and RAM.
Error-correcting codes are usually distinguished between convolutional codes and block codes:

Convolutional codes are processed on a bit-by-bit basis. They are particularly suitable for implementation in hardware, and the Viterbi decoder allows optimal decoding.
Block codes are processed on a block-by-block basis. Early examples of block codes are repetition codes, Hamming codes and multidimensional parity-check codes. They were followed by a number of efficient codes, Reed–Solomon codes being the most notable due to their current widespread use. Turbo codes and low-density parity-check codes (LDPC) are relatively new constructions that can provide almost optimal efficiency.
Shannon's theorem is an important theorem in forward error correction, and describes the maximum information rate at which reliable communication is possible over a channel that has a certain error probability or signal-to-noise ratio (SNR). This strict upper limit is expressed in terms of the channel capacity. More specifically, the theorem says that there exist codes such that with increasing encoding length the probability of error on a discrete memoryless channel can be made arbitrarily small, provided that the code rate is lower than the channel capacity. The code rate is defined as the fraction k/n of k source symbols and n encoded symbols.
The actual maximum code rate allowed depends on the error-correcting code used, and may be lower. This is because Shannon's proof was only of existential nature, and did not show how to construct codes that are both optimal and have efficient encoding and decoding algorithms.


=== Hybrid schemes ===

Hybrid ARQ is a combination of ARQ and forward error correction.""",
    tier=7,
    domain="methodology",
    source="Wikipedia, 'Error detection and correction'",
    source_url="https://en.wikipedia.org/wiki/Error_detection_and_correction",
))

register_atom(Atom(
    atom_type="identity",
    name="derive_identity",
    content="""In trigonometry, trigonometric identities are equalities that involve trigonometric functions and are true for every value of the occurring variables for which both sides of the equality are defined. Geometrically, these are identities involving certain functions of one or more angles. They are distinct from triangle identities, which are identities potentially involving angles but also involving side lengths or other lengths of a triangle.
These identities are useful whenever expressions involving trigonometric functions need to be simplified. An important application is the integration of non-trigonometric functions: a common technique involves first using the substitution rule with a trigonometric function, and then simplifying the resulting integral with a trigonometric identity.


== Pythagorean identities ==

The basic relationship between the sine and cosine is given by the Pythagorean identity:

  
    
      
        
          sin
          
            2
          
        
        ⁡
        θ
        +
        
          cos
          
            2
          
        
        ⁡
        θ
        =
        1
        ,
      
    
    {\\displaystyle \\sin ^{2}\\theta +\\cos ^{2}\\theta =1,}
  

where 
  
    
      
        
          sin
          
            2
          
        
        ⁡
        θ
      
    
    {\\displaystyle \\sin ^{2}\\theta }
  
 means 
  
    
      
        
          
            (
            sin
            ⁡
            θ
            )
          
          
            2
          
        
      
    
    {\\displaystyle {(\\sin \\theta )}^{2}}
  
 and 
  
    
      
        
          cos
          
            2
          
        
        ⁡
        θ
      
    
    {\\displaystyle \\cos ^{2}\\theta }
  
 means 
  
    
      
        
          
            (
            cos
            ⁡
            θ
            )
          
          
            2
          
        
        .
      
    
    {\\displaystyle {(\\cos \\theta )}^{2}.}
  

This can be viewed as a version of the Pythagorean theorem, and follows from the equation 
  
    
      
        
          x
          
            2
          
        
        +
        
          y
          
            2
          
        
        =
        1
      
    
    {\\displaystyle x^{2}+y^{2}=1}
  
 for the unit circle. This equation can be solved for either the sine or the cosine:

  
    
      
        
          
            
              
                sin
                ⁡
                θ
              
              
                
                =
                ±
                
                  
                    1
                    −
                    
                      cos
                      
                        2
                      
                    
                    ⁡
                    θ
                  
                
                ,
              
            
            
              
                cos
                ⁡
                θ
              
              
                
                =
                ±
                
                  
                    1
                    −
                    
                      sin
                      
                        2
                      
                    
                    ⁡
                    θ
                  
                
                .
              
            
          
        
      
    
    {\\displaystyle {\\begin{aligned}\\sin \\theta &=\\pm {\\sqrt {1-\\cos ^{2}\\theta }},\\\\\\cos \\theta &=\\pm {\\sqrt {1-\\sin ^{2}\\theta }}.\\end{aligned}}}
  

where the sign depends on the quadrant of 
  
    
      
        θ
        .
      
    
    {\\displaystyle \\theta .}
  

Dividing this identity by 
  
    
      
        
          sin
          
            2
          
        
        ⁡
        θ
      
    
    {\\displaystyle \\sin ^{2}\\theta }
  
, 
  
    
      
        
          cos
          
            2
          
        
        ⁡
        θ
      
    
    {\\displaystyle \\cos ^{2}\\theta }
  
, or both yields the following identities:

  
    
      
        
          
            
              
                1
                +
                
                  cot
                  
                    2
                  
                
                ⁡
                θ
              
              
                
                =
                
                  csc
                  
                    2
                  
                
                ⁡
                θ
              
            
            
              
                1
                +
                
                  tan
                  
                    2
                  
                
                ⁡
                θ
              
              
                
                =
                
                  sec
                  
                    2
                  
                
                ⁡
                θ
              
            
            
              
                
                  sec
                  
                    2
                  
                
                ⁡
                θ
                +
                
                  csc
                  
                    2
                  
                
                ⁡
                θ
              
              
                
                =
                
                  sec
                  
                    2
                  
                
                ⁡
                θ
                
                  csc
                  
                    2
                  
                
                ⁡
                θ
              
            
          
        
      
    
    {\\displaystyle {\\begin{aligned}1+\\cot ^{2}\\theta &=\\csc ^{2}\\theta \\\\1+\\tan ^{2}\\theta &=\\sec ^{2}\\theta \\\\\\sec ^{2}\\theta +\\csc ^{2}\\theta &=\\sec ^{2}\\theta \\csc ^{2}\\theta \\end{aligned}}}
  

Using these identities, it is possible to express any trigonometric function in terms of any other (up to a plus or minus sign):


== Reflections, shifts, and periodicity ==
By examining the unit circle, one can establish the following properties of the trigonometric functions.


=== Reflections ===

When the direction of a Euclidean vector is represented by an angle 
  
    
      
        θ
        ,
      
    
    {\\displaystyle \\theta ,}
  
 this is the angle determined by the free vector (starting at the origin) and the positive 
  
    
      
        x
      
    
    {\\displaystyle x}
  
-unit vector. The same concept may also be applied to lines in an Euclidean space, where the angle is that determined by a parallel to the given line through the origin and the positive 
  
    
      
        x
      
    
    {\\displaystyle x}
  
-axis.""",
    tier=7,
    domain="algebra",
    source="Wikipedia, 'List of trigonometric identities'",
    source_url="https://en.wikipedia.org/wiki/List_of_trigonometric_identities",
))

register_atom(Atom(
    atom_type="principle",
    name="construct_polynomial",
    content="""In numerical analysis, polynomial interpolation is the interpolation of a given data set by the polynomial of lowest possible degree that passes through the points in the dataset.
Given a set of n + 1 data points 
  
    
      
        (
        
          x
          
            0
          
        
        ,
        
          y
          
            0
          
        
        )
        ,
        …
        ,
        (
        
          x
          
            n
          
        
        ,
        
          y
          
            n
          
        
        )
      
    
    {\\displaystyle (x_{0},y_{0}),\\ldots ,(x_{n},y_{n})}
  
, with no two 
  
    
      
        
          x
          
            j
          
        
      
    
    {\\displaystyle x_{j}}
  
 the same, a polynomial function 
  
    
      
        p
        (
        x
        )
        =
        
          a
          
            0
          
        
        +
        
          a
          
            1
          
        
        x
        +
        ⋯
        +
        
          a
          
            n
          
        
        
          x
          
            n
          
        
      
    
    {\\displaystyle p(x)=a_{0}+a_{1}x+\\cdots +a_{n}x^{n}}
  
 is said to interpolate the data if 
  
    
      
        p
        (
        
          x
          
            j
          
        
        )
        =
        
          y
          
            j
          
        
      
    
    {\\displaystyle p(x_{j})=y_{j}}
  
 for each 
  
    
      
        j
        ∈
        {
        0
        ,
        1
        ,
        …
        ,
        n
        }
      
    
    {\\displaystyle j\\in \\{0,1,\\dotsc ,n\\}}
  
.
There is always a unique such polynomial, commonly given by two explicit formulas, the Lagrange polynomials and Newton polynomials.


== Applications ==
The original use of interpolation polynomials was to approximate values of important transcendental functions such as natural logarithm and trigonometric functions. Starting with a few accurately computed data points, the corresponding interpolation polynomial will approximate the function at an arbitrary nearby point. Polynomial interpolation also forms the basis for algorithms in numerical quadrature (Simpson's rule) and numerical ordinary differential equations (multigrid methods).
In computer graphics, polynomials can be used to approximate complicated plane curves given a few specified points, for example the shapes of letters in typography. This is usually done with Bézier curves, which are a simple generalization of interpolation polynomials (having specified tangents as well as specified points).
In numerical analysis, polynomial interpolation is essential to perform sub-quadratic multiplication and squaring, such as Karatsuba multiplication and Toom–Cook multiplication, where interpolation through points on a product polynomial yields the specific product required. For example, given a = f(x) = a0x0 + a1x1 + ··· and b = g(x) = b0x0 + b1x1 + ···, the product ab is a specific value of W(x) = f(x)g(x). One may easily find points along W(x) at small values of x, and interpolation based on those points will yield the terms of W(x) and the specific product ab. As fomulated in Karatsuba multiplication, this technique is substantially faster than quadratic multiplication, even for modest-sized inputs, especially on parallel hardware.
In computer science, polynomial interpolation also leads to algorithms for secure multi party computation and secret sharing.


== Interpolation theorem ==
For any 
  
    
      
        n
        +
        1
      
    
    {\\displaystyle n+1}
  
 bivariate data points 
  
    
      
        (
        
          x
          
            0
          
        
        ,
        
          y
          
            0
          
        
        )
        ,
        …
        ,
        (
        
          x
          
            n
          
        
        ,
        
          y
          
            n
          
        
        )
        ∈
        
          
            R
          
          
            2
          
        
      
    
    {\\displaystyle (x_{0},y_{0}),\\dotsc ,(x_{n},y_{n})\\in \\mathbb {R} ^{2}}
  
, where no two 
  
    
      
        
          x
          
            j
          
        
      
    
    {\\displaystyle x_{j}}
  
 are the same, there exists a unique polynomial 
  
    
      
        p
        (
        x
        )
      
    
    {\\displaystyle p(x)}
  
 of degree at most 
  
    
      
        n
      
    
    {\\displaystyle n}
  
 that interpolates these points, i.e. 
  
    
      
        p
        (
        
          x
          
            0
          
        
        )
        =
        
          y
          
            0
          
        
        ,
        …
        ,
        p
        (
        
          x
          
            n
          
        
        )
        =
        
          y
          
            n
          
        
      
    
    {\\displaystyle p(x_{0})=y_{0},\\ldots ,p(x_{n})=y_{n}}
  
.
Equivalently, for a fixed choice of interpolation nodes 
  
    
      
        
          x
          
            j
          
        
      
    
    {\\displaystyle x_{j}}
  
, polynomial interpolation defines a linear bijection 
  
    
      
        
          L
          
            n
          
        
      
    
    {\\displaystyle L_{n}}
  
 between the (n+1)-tuples of real-number values 
  
    
      
        (
        
          y
          
            0
          
        
        ,
        …
        ,
        
          y
          
            n
          
        
        )
        ∈
        
          
            R
          
          
            n
            +
            1
          
        
      
    
    {\\displaystyle (y_{0},\\ldots ,y_{n})\\in \\mathbb {R} ^{n+1}}
  
 and the vector space 
  
    
      
        P
        (
        n
        )
      
    
    {\\displaystyle P(n)}
  
 of real polynomials of degree at most n:

  
    
      
        
          L
          
            n
          
        
        :
        
          
            R
          
          
            n
            +
            1
          
        
        
          
            
              
                ⟶
              
              
                ∼
              
            
          
        
        
        P
        (
        n
        )
        .
      
    
    {\\displaystyle L_{n}:\\mathbb {R} ^{n+1}{\\stackrel {\\sim }{\\longrightarrow }}\\,P(n).}
  

This is a type of unisolvence theorem.""",
    tier=7,
    domain="algebra",
    source="Wikipedia, 'Polynomial interpolation'",
    source_url="https://en.wikipedia.org/wiki/Polynomial_interpolation",
))

register_atom(Atom(
    atom_type="principle",
    name="generalise_sequence",
    content="""In mathematics, a sequence is a collection of objects possibly with repetition, that come in a specified order. Like a set, it contains members (also called elements, or terms). Unlike a set, the same elements can appear multiple times at different positions in a sequence, and unlike a set, the order does matter. The notion of a sequence can be generalized to an indexed family, defined as a function from an arbitrary index set.
For example, (M, A, R, Y) is a sequence of letters with the letter "M" first and "Y" last. This sequence differs from (A, R, M, Y). Also, the sequence (1, 1, 2, 3, 5, 8), which contains the number 1 at two different positions, is a valid sequence. Sequences can be finite, as in these examples, or infinite, such as the sequence of positive even integers (2, 4, 6, 8, ...).
The length of a finite sequence is defined as the number of elements in the sequence. The position of an element in a sequence is its rank or index; it is the natural number for which the element is the image. The first element typically has index 0 or 1. In mathematical analysis, a sequence is often denoted by letters in the form of 
  
    
      
        
          a
          
            n
          
        
      
    
    {\\displaystyle a_{n}}
  
, 
  
    
      
        
          b
          
            n
          
        
      
    
    {\\displaystyle b_{n}}
  
 and 
  
    
      
        
          c
          
            n
          
        
      
    
    {\\displaystyle c_{n}}
  
, where the subscript n refers to the nth element of the sequence; for example, the nth element of the Fibonacci sequence 
  
    
      
        F
      
    
    {\\displaystyle F}
  
 is generally denoted as 
  
    
      
        
          F
          
            n
          
        
      
    
    {\\displaystyle F_{n}}
  
.
In computing and computer science, finite sequences are usually called strings, words or lists, with the specific technical term chosen depending on the type of object the sequence enumerates and the different ways to represent the sequence in computer memory. Infinite sequences are called streams.
The empty sequence ( ) is included in most notions of sequence. It may be excluded depending on the context.


== Examples and notation ==
A sequence can be thought of as a list of elements with a particular order. Sequences are useful in a number of mathematical disciplines for studying functions, spaces, and other mathematical structures using the convergence properties of sequences. In particular, sequences are the basis for series, which are important in differential equations and analysis. Sequences are also of interest in their own right, and can be studied as patterns or puzzles, such as in the study of prime numbers.
There are a number of ways to denote a sequence, some of which are more useful for specific types of sequences. One way to specify a sequence is to list all its elements. For example, the first four odd integers form the sequence (1, 3, 5, 7). This notation is used for infinite sequences as well. For instance, the infinite sequence of positive odd integers is written as (1, 3, 5, 7, ...). Because notating sequences with ellipsis leads to ambiguity, listing is most useful for customary infinite sequences which can be easily recognized from their first few elements. Other ways of denoting a sequence are discussed after the examples.


=== Examples ===

A prime number is a natural numbers greater than 1 that has no divisors except 1 and itself. Listing the prime numbers in their natural order gives the sequence (2, 3, 5, 7, 11, 13, 17, ...). The prime numbers are widely used in mathematics, particularly in number theory where many results related to them exist.
The Fibonacci numbers are a sequence for which each element is the sum of the previous two elements. The zeroth and first elements are 0 and 1, so the sequence is (0, 1, 1, 2, 3, 5, 8, 13, ...).
Other sequences have rational numbers as elements. The sequence (.9, .99, .999, .9999, ...), for instance, approaches the number 1. As another example, π is the limit of the sequence (3, 3.1, 3.14, 3.141, 3.1415, ...), which is increasing. In fact, every real number can be written as the limit of a sequence of rational numbers (e.g. via its decimal expansion, also see completeness of the real numbers). A related type of sequence consists of the decimal digits of a real number, for example the sequence of digits of π, (3, 1, 4, 1, 5, 9, ...). This sequence does not have any pattern that is easily discernible by inspection.
The elements of a sequence can be functions instead of numbers. For example, the monomial basis for polynomials of a single variable forms the sequence 
  
    
      
        (
        x
        ↦
        1
        ,
        x
        ↦
        x
        ,
        x
        ↦
        
          x
          
            2
          
        
        ,
        x
        ↦
        
          x
          
            3
          
        
        ,
        …
        )
      
    
    {\\displaystyle (x\\mapsto 1,x\\mapsto x,x\\mapsto x^{2},x\\mapsto x^{3},\\ldots )}
  
, using arrow notation.
The On-Line Encyclopedia of Integer Sequences comprises a large list of examples of integer sequences.


=== Indexing ===
Other notations can be useful for sequences whose pattern cannot be easily guessed or for sequences that do not have a pattern, such as the digits of π. One such notation is to write down a general formula for computing the nth term as a function of n, enclose it in parentheses, and include a subscript indicating the set of values that n can take. For example, in this notation the sequence of even integers could be written as 
  
    
      
        (
        2
        n
        
          )
          
            n
            ∈
            
              N
            
          
        
      
    
    {\\displaystyle (2n)_{n\\in \\mathbb {N} }}
  
, where ⁠
  
    
      
        
          N
        
      
    
    {\\displaystyle \\mathbb {N} }
  
⁠ denotes the set of natural numbers. The sequence of square numbers could be written as 
  
    
      
        (
        
          n
          
            2
          
        
        
          )
          
            n
            ∈
            
              N
            
          
        
      
    
    {\\textstyle (n^{2})_{n\\in \\mathbb {N} }}
  
. The variable n is called an index, and the set of values that it can take is called the index set.
It is often useful to combine this notation with the technique of treating the elements of a sequence as individual variables. This yields expressions like 
  
    
      
        (
        
          a
          
            n
          
        
        
          )
          
            n
            ∈
            
              N
            
          
        
      
    
    {\\displaystyle (a_{n})_{n\\in \\mathbb {N} }}
  
, which denotes a sequence whose nth element is given by the variable 
  
    
      
        
          a
          
            n
          
        
      
    
    {\\displaystyle a_{n}}
  
.""",
    tier=7,
    domain="algebra",
    source="Wikipedia, 'Sequence'",
    source_url="https://en.wikipedia.org/wiki/Sequence",
))

register_atom(Atom(
    atom_type="principle",
    name="counterexample",
    content="""A counterexample is a specific example that contradicts a claim, hypothesis, or generalization. In logic a counterexample disproves a universally stated claim, and does so rigorously in the fields of mathematics and philosophy. For example, the statement that "student John Smith is not lazy" is a counterexample to the generalization "students are lazy", and both a counterexample to, and disproof of, the universally quantified "all students are lazy."


== In mathematics ==
In mathematics, counterexamples are often used to prove the boundaries of possible theorems. By using counterexamples to show that certain conjectures are false, mathematical researchers can then avoid going down blind alleys and learn to modify conjectures to produce provable theorems. It is sometimes said that mathematical development consists primarily in finding (and proving) theorems and counterexamples.


=== Rectangle example ===
Suppose that a mathematician is studying geometry and shapes, and she wishes to prove certain theorems about them. She conjectures that "All rectangles are squares", and she is interested in knowing whether this statement is true or false. 
In this case, she can either attempt to prove the truth of the statement using deductive reasoning, or she can attempt to find a counterexample of the statement if she suspects it to be false. In the latter case, a counterexample would be a rectangle that is not a square, such as a rectangle with two sides of length 5 and two sides of length 7. However, despite having found rectangles that were not squares, all the rectangles she did find had four sides. She then makes the new conjecture "All rectangles have four sides". This is logically weaker than her original conjecture, since every square has four sides, but not every four-sided shape is a square.
The above example explained — in a simplified way — how a mathematician might weaken her conjecture in the face of counterexamples, but counterexamples can also be used to demonstrate the necessity of certain assumptions and hypothesis. For example, suppose that after a while, the mathematician above settled on the new conjecture "All shapes that are rectangles and have four sides of equal length are squares". This conjecture has two parts to the hypothesis: the shape must be 'a rectangle' and must have  'four sides of equal length'. The mathematician then would like to know if she can remove either assumption, and still maintain the truth of her conjecture. This means that she needs to check the truth of the following two statements:

"All shapes that are rectangles are squares."
"All shapes that have four sides of equal length are squares".
A counterexample to (1) was already given above, and a counterexample to (2) is a non-square rhombus. Thus, the mathematician now knows that each assumption by itself is insufficient.


=== Other mathematical examples ===

A counterexample to the statement "all prime numbers are odd numbers" is the number 2, as it is a prime number but is not an odd number. Neither of the numbers 7 or 10 is a counterexample, as neither of them are enough to contradict the statement. In this example, 2 is in fact the only possible counterexample to the statement, even though that alone is enough to contradict the statement. In a similar manner, the statement "All natural numbers are either prime or composite" has the number 1 as a counterexample, as 1 is neither prime nor composite.
Euler's sum of powers conjecture was disproved by counterexample. It asserted that at least n nth powers were necessary to sum to another nth power. This conjecture was disproved in 1966, with a counterexample involving n = 5; other n = 5 counterexamples are now known, as well as some n = 4 counterexamples.
Witsenhausen's counterexample shows that it is not always true (for control problems) that a quadratic loss function and a linear equation of evolution of the state variable imply optimal control laws that are linear.
All Euclidean plane isometries are mappings that preserve area, but the converse is false as shown by counterexamples shear mapping and squeeze mapping.
Other examples include the disproofs of the Seifert conjecture, the Pólya conjecture, the conjecture of Hilbert's fourteenth problem, Tait's conjecture, and the Ganea conjecture.


== In philosophy ==
In philosophy, counterexamples are usually used to argue that a certain philosophical position is wrong by showing that it does not apply in certain cases. Alternatively, the first philosopher can modify their claim so that the counterexample no longer applies; this is analogous to when a mathematician modifies a conjecture because of a counterexample.
For example, in Plato's Gorgias, Callicles argues that those who are physically stronger or more capable are naturally entitled to rule over weaker people.  Socrates responds by proposing that the sheer number of ordinary people, by virtue of their combined strength, could be considered "stronger" than the aristocratic few even though the masses are prima facie of worse character. This presents a counterexample Callicles' claim, by shifting the notion of strength from individual superiority to collective power.  Callicles' argument therefore fails under this alternative interpretation, unless he revises his claim.
Callicles might challenge Socrates' counterexample, arguing perhaps that the common rabble really are better than the nobles, or that even in their large numbers, they still are not stronger. But if Callicles accepts the counterexample, then he must either withdraw his claim, or modify it so that the counterexample no longer applies. For example, he might modify his claim to refer only to individual persons, requiring him to think of the common people as a collection of individuals rather than as a mob. As it happens, he modifies his claim to say "wiser" instead of "stronger", arguing that no amount of numerical superiority can make people wiser.


== See also ==
Contradiction
Exception that proves the rule
Minimal counterexample


== References ==


== Further reading ==
Imre Lakatos, Proofs and Refutations (1976) Cambridge University Press ISBN 0521290384
James Franklin and Albert Daoud (2011) Proof in Mathematics: An Introduction, Kew, Sydney ISBN 978-0-646-54509-7, ch. 6.
Lynn Arthur Steen and J. Arthur Seebach, Jr. (1978) Counterexamples in Topology, Springer, New York ISBN 0-486-68735-X.
Joseph P. Romano and Andrew F. Siegel (1986) Counterexamples in Probability and Statistics Chapman & Hall, New York, London ISBN 0-412-98901-8.
Gary L. Wise and Eric B. Hall (1993) Counterexamples in Probability and Real Analysis. Oxford University Press, New York ISBN 0-19-507068-2.
Bernard R. Gelbaum, John M. H. Olmsted (2003) Counterexamples in Analysis. Corrected reprint of the second (1965) edition, Dover Publications, Mineola, NY ISBN 0-486-42875-3.
Jordan M. Stoyanov (1997) Counterexamples in Probability Second edition, Wiley, Chichester ISBN 0-471-96538-3.
Michael Copobianco & John Mulluzzo (1978) Examples and Counterexamples in Graph Theory, Elsevier North-Holland ISBN 0-444-00255-3.


== External links ==
 Quotations related to Counterexample at Wikiquote""",
    tier=7,
    domain="logic",
    source="Wikipedia, 'Counterexample'",
    source_url="https://en.wikipedia.org/wiki/Counterexample",
))

register_atom(Atom(
    atom_type="methodology",
    name="inverse_problem",
    content="""An inverse problem in science is the process of calculating from a set of observations the causal factors that produced them: for example, calculating an image in X-ray computed tomography, source reconstruction in acoustics, or calculating the density of the Earth from measurements of its gravity field. It is called an inverse problem because it starts with the effects and then calculates the causes. It is the inverse of a forward problem, which starts with the causes and then calculates the effects.
Inverse problems are some of the most important mathematical problems in science and mathematics because they tell us about parameters that we cannot directly observe. They can be found in system identification, optics, radar, acoustics, communication theory, signal processing, medical imaging, computer vision, geophysics, oceanography, meteorology, astronomy, remote sensing, natural language processing, machine learning, nondestructive testing, slope stability analysis and many other fields.


== History ==
Starting with the effects to discover the causes has concerned physicists for centuries. A historical example is the calculations of Adams and Le Verrier which led to the discovery of Neptune from the perturbed trajectory of Uranus. However, a formal study of inverse problems was not initiated until the 20th century.
One of the earliest examples of a solution to an inverse problem was discovered by Hermann Weyl and published in 1911, describing the asymptotic behavior of eigenvalues of the Laplace–Beltrami operator. Today known as Weyl's law, it is perhaps most easily understood as an answer to the question of whether it is possible to hear the shape of a drum. Weyl conjectured that the eigenfrequencies of a drum would be related to the area and perimeter of the drum by a particular equation, a result improved upon by later mathematicians.
The field of inverse problems was later touched on by Soviet-Armenian physicist, Viktor Ambartsumian.
While still a student, Ambartsumian thoroughly studied the theory of atomic structure, the formation of energy levels, and the Schrödinger equation and its properties, and when he mastered the theory of eigenvalues of differential equations, he pointed out the apparent analogy between discrete energy levels and the eigenvalues of differential equations. He then asked: given a family of eigenvalues, is it possible to find the form of the equations whose eigenvalues they are? Essentially Ambartsumian was examining the inverse Sturm–Liouville problem, which dealt with determining the equations of a vibrating string. This paper was published in 1929 in the German physics journal Zeitschrift für Physik and remained in obscurity for a rather long time. Describing this situation after many decades, Ambartsumian said, "If an astronomer publishes an article with a mathematical content in a physics journal, then the most likely thing that will happen to it is oblivion."
Nonetheless, toward the end of the Second World War, this article, written by the 20-year-old Ambartsumian, was found by Swedish mathematicians and formed the starting point for a whole area of research on inverse problems, becoming the foundation of an entire discipline.
Then important efforts have been devoted to a "direct solution" of the inverse scattering problem especially by Gelfand and Levitan in the Soviet Union. They proposed an analytic constructive method for determining the solution.  When computers became available, some authors have investigated the possibility of applying their approach to similar problems such as the inverse problem in the 1D wave equation. But it rapidly turned out that the inversion is an unstable process: noise and errors can be tremendously amplified making a direct solution hardly practicable.
Then, around the seventies, the least-squares and probabilistic approaches came in and turned out to be very helpful for the determination of parameters involved in various physical systems. This approach met a lot of success. Nowadays inverse problems are also investigated in fields outside physics, such as chemistry, economics, and computer science. Eventually, as numerical models become prevalent in many parts of society, we may expect an inverse problem associated with each of these numerical models.


== Conceptual understanding ==
Since Newton, scientists have extensively attempted to model the world. In particular, when a mathematical model is available (for instance, Newton's gravitational law or Coulomb's equation for electrostatics), we can foresee, given some parameters that describe a physical system (such as a distribution of mass or a distribution of electric charges), the behavior of the system. This approach is known as mathematical modeling and the above-mentioned physical parameters are called the model parameters or simply the model. To be precise, we introduce the notion of state of the physical system: it is the solution of the mathematical model's equation. In optimal control theory, these equations are referred to as the state equations. In many situations we are not truly interested in knowing the physical state but just its effects on some objects (for instance, the effects the gravitational field has on a specific planet). Hence we have to introduce another operator, called the observation operator, which converts the state of the physical system (here the predicted gravitational field) into what we want to observe (here the movements of the considered planet). We can now introduce the so-called forward problem, which consists of two steps:

determination of the state of the system from the physical parameters that describe it
application of the observation operator to the estimated state of the system so as to predict the behavior of what we want to observe.
This leads to introduce another operator 
  
    
      
        F
      
    
    {\\displaystyle F}
  
 (F stands for "forward") which maps model parameters 
  
    
      
        p
      
    
    {\\displaystyle p}
  
 into 
  
    
      
        F
        (
        p
        )
      
    
    {\\displaystyle F(p)}
  
, the data that model 
  
    
      
        p
      
    
    {\\displaystyle p}
  
 predicts that is the result of this two-step procedure. Operator 
  
    
      
        F
      
    
    {\\displaystyle F}
  
 is called forward operator or forward map.
In this approach we basically attempt at predicting the effects knowing the causes.
The table below shows, the Earth being considered as the physical system and for different physical phenomena, the model parameters that describe the system, the physical quantity that describes the state of the physical system and observations commonly made on the state of the system. 

In the inverse problem approach we, roughly speaking, try to know the causes given the effects.


== General statement of the inverse problem ==
The inverse problem is the "inverse" of the forward problem: instead of determining the data produced by particular model parameters, we want to determine the model parameters that produce the data 
  
    
      
        
          d
          
            obs
          
        
      
    
    {\\displaystyle d_{\\text{obs}}}
  
 that is the observation we have recorded (the subscript obs stands for observed).
Our goal, in other words, is to determine the model parameters 
  
    
      
        p
      
    
    {\\displaystyle p}
  
 such that (at least approximately)

  
    
      
        
          d
          
            obs
          
        
        =
        F
        (
        p
        )
      
    
    {\\displaystyle d_{\\text{obs}}=F(p)}
  

where 
  
    
      
        F
      
    
    {\\displaystyle F}
  
 is the forward map.""",
    tier=7,
    domain="calculus",
    source="Wikipedia, 'Inverse problem'",
    source_url="https://en.wikipedia.org/wiki/Inverse_problem",
))

register_atom(Atom(
    atom_type="methodology",
    name="method_selection",
    content="""Problem solving is the process of achieving a goal by overcoming obstacles, a frequent part of most activities. Problems in need of solutions range from simple personal tasks (e.g. how to turn on an appliance) to complex issues in business and technical fields. The former is an example of simple problem solving (SPS) addressing one issue, whereas the latter is complex problem solving (CPS) with multiple interrelated obstacles. Another classification of problem-solving tasks is into well-defined problems with specific obstacles and goals, and ill-defined problems in which the current situation is troublesome but it is not clear what kind of resolution to aim for. Similarly, one may distinguish formal or fact-based problems requiring psychometric intelligence, versus socio-emotional problems which depend on the changeable emotions of individuals or groups, such as tactful behavior, fashion, or gift choices.
Solutions require sufficient resources and knowledge to attain the goal. Professionals such as lawyers, doctors, programmers, and consultants are largely problem solvers for issues that require technical skills and knowledge beyond general competence. Many businesses have found profitable markets by recognizing a problem and creating a solution: the more widespread and inconvenient the problem, the greater the opportunity to develop a scalable solution.
There are many specialized problem-solving techniques and methods in fields such as science, engineering, business, medicine, mathematics, computer science, philosophy, and social organization. The mental techniques to identify, analyze, and solve problems are studied in psychology and cognitive sciences. Also widely researched are the mental obstacles that prevent people from finding solutions; problem-solving impediments include confirmation bias, mental set, and functional fixedness.


== Definition ==
The term problem solving has a slightly different meaning depending on the discipline. For instance, it is a mental process in psychology and a computerized process in computer science. There are two different types of problems: ill-defined and well-defined; different approaches are used for each. Well-defined problems have specific end goals and clearly expected solutions, while ill-defined problems do not. Well-defined problems allow for more initial planning than ill-defined problems. Solving problems sometimes involves dealing with pragmatics (the way that context contributes to meaning) and semantics (the interpretation of the problem). The ability to understand what the end goal of the problem is, and what rules could be applied, represents the key to solving the problem. Sometimes a problem requires abstract thinking or coming up with a creative solution.
Problem solving has two major domains: mathematical problem solving and personal problem solving. Each concerns some difficulty or barrier that is encountered.


=== Psychology ===
Problem solving in psychology refers to the process of finding solutions to problems encountered in life. Solutions to these problems are usually situation- or context-specific. The process starts with problem finding and problem shaping, in which the problem is discovered and simplified. The next step is to generate possible solutions and evaluate them. Finally a solution is selected to be implemented and verified. Problems have an end goal to be reached; how you get there depends upon problem orientation (problem-solving coping style and skills) and systematic analysis.
Mental health professionals study the human problem-solving processes using methods such as introspection, behaviorism, simulation, computer modeling, and experiment. Social psychologists look into the person-environment relationship aspect of the problem and independent and interdependent problem-solving methods. Problem solving has been defined as a higher-order cognitive process and intellectual function that requires the modulation and control of more routine or fundamental skills.
Empirical research shows many different strategies and factors influence everyday problem solving. Rehabilitation psychologists studying people with frontal lobe injuries have found that deficits in emotional control and reasoning can be re-mediated with effective rehabilitation and could improve the capacity of injured persons to resolve everyday problems. Interpersonal everyday problem solving is dependent upon personal motivational and contextual components. One such component is the emotional valence of "real-world" problems, which can either impede or aid problem-solving performance. Researchers have focused on the role of emotions in problem solving, demonstrating that poor emotional control can disrupt focus on the target task, impede problem resolution, and lead to negative outcomes such as fatigue, depression, and inertia. In conceptualization,human problem solving consists of two related processes: problem orientation, and the motivational/attitudinal/affective approach to problematic situations and problem-solving skills. People's strategies cohere with their goals and stem from the process of comparing oneself with others.


=== Cognitive sciences ===
Among the first experimental psychologists to study problem solving were the Gestaltists in Germany, such as Karl Duncker in The Psychology of Productive Thinking (1935). Perhaps best known is the work of Allen Newell and Herbert A. Simon.
Experiments in the 1960s and early 1970s asked participants to solve relatively simple, well-defined, but not previously seen laboratory tasks. These simple problems, such as the Tower of Hanoi, admitted optimal solutions that could be found quickly, allowing researchers to observe the full problem-solving process. Researchers assumed that these model problems would elicit the characteristic cognitive processes by which more complex "real world" problems are solved.
An outstanding problem-solving technique found by this research is the principle of decomposition.


=== Computer science ===

Much of computer science and artificial intelligence involves designing automated systems to solve a specified type of problem: to accept input data and calculate a correct or adequate response, reasonably quickly. Algorithms are recipes or instructions that direct such systems, written into computer programs.
Steps for designing such systems include problem determination, heuristics, root cause analysis, de-duplication, analysis, diagnosis, and repair. Analytic techniques include linear and nonlinear programming, queuing systems, and simulation. A large, perennial obstacle is to find and fix errors in computer programs: debugging.


=== Logic ===
Formal logic concerns issues like validity, truth, inference, argumentation, and proof. In a problem-solving context, it can be used to formally represent a problem as a theorem to be proved, and to represent the knowledge needed to solve the problem as the premises to be used in a proof that the problem has a solution.
The use of computers to prove mathematical theorems using formal logic emerged as the field of automated theorem proving in the 1950s. It included the use of heuristic methods designed to simulate human problem solving, as in the Logic Theory Machine, developed by Allen Newell, Herbert A. Simon and J. C. Shaw, as well as algorithmic methods such as the resolution principle developed by John Alan Robinson.
In addition to its use for finding proofs of mathematical theorems, automated theorem-proving has also been used for program verification in computer science. In 1958, John McCarthy proposed the advice taker, to represent information in formal logic and to derive answers to questions using automated theorem-proving.""",
    tier=7,
    domain="methodology",
    source="Wikipedia, 'Problem solving'",
    source_url="https://en.wikipedia.org/wiki/Problem_solving",
))

register_atom(Atom(
    atom_type="principle",
    name="estimate_magnitude",
    content="""A Fermi problem (or Fermi question, Fermi quiz), also known as an order-of-magnitude problem, is an estimation problem in physics or engineering education, designed to teach dimensional analysis or approximation of extreme scientific calculations. Fermi problems are usually back-of-the-envelope calculations. Fermi problems typically involve making justified guesses about quantities and their variance or lower and upper bounds. In some cases, order-of-magnitude estimates can also be derived using dimensional analysis. A Fermi estimate (or order-of-magnitude estimate, order estimation) is an estimate of an extreme scientific calculation.


== Historical background ==
The estimation technique is named after physicist Enrico Fermi as he was known for his ability to make good approximate calculations with little or no actual data. An example is Enrico Fermi's estimate of the strength of the atomic bomb that detonated at the Trinity test, based on the distance traveled by pieces of paper he dropped from his hand during the blast. Fermi's estimate of 10 kilotons of TNT was well within an order of magnitude of the now-accepted value of 21 kilotons.


== Justification ==
Fermi estimates generally work because the estimations of the individual terms are often close to correct, and overestimates and underestimates help cancel each other out. That is, if there is no consistent bias, a Fermi calculation that involves the multiplication of several estimated factors (such as the number of piano tuners in Chicago) will probably be more accurate than might be first supposed.
In detail, multiplying estimates corresponds to adding their logarithms; thus one obtains a sort of Wiener process or random walk on the logarithmic scale, which diffuses as 
  
    
      
        
          
            n
          
        
      
    
    {\\displaystyle {\\sqrt {n}}}
  
 (in number of terms n). In discrete terms, the number of overestimates minus underestimates will have a binomial distribution. In continuous terms, if one makes a Fermi estimate of n steps, with standard deviation σ units on the log scale from the actual value, then the overall estimate will have standard deviation 
  
    
      
        σ
        
          
            n
          
        
      
    
    {\\displaystyle \\sigma {\\sqrt {n}}}
  
, since the standard deviation of a sum scales as 
  
    
      
        
          
            n
          
        
      
    
    {\\displaystyle {\\sqrt {n}}}
  
 in the number of summands.
For instance, if one makes a 9-step Fermi estimate, at each step overestimating or underestimating the correct number by a factor of 2 (or with a standard deviation 2), then after 9 steps the standard error will have grown by a logarithmic factor of 
  
    
      
        
          
            9
          
        
        =
        3
      
    
    {\\displaystyle {\\sqrt {9}}=3}
  
, so 23 = 8. Thus one will expect to be within 1⁄8 to 8 times the correct value – within an order of magnitude, and much less than the worst case of erring by a factor of 29 = 512 (about 2.71 orders of magnitude). If one has a shorter chain or estimates more accurately, the overall estimate will be correspondingly better.


== Examples ==
Fermi questions are often extreme in nature, and cannot usually be solved using common mathematical or scientific information.
Example questions given by the official Fermi Competition:

"If the mass of one teaspoon of water could be converted entirely into energy in the form of heat, what volume of water, initially at room temperature, could it bring to a boil? (litres).""How much does the Thames River heat up in going over the Fanshawe Dam? (Celsius degrees).""What is the mass of all the automobiles scrapped in North America this month? (kilograms)."
Possibly the most famous order-of-magnitude problem is the Fermi paradox, which considers the odds of a significant number of intelligent civilizations existing in the galaxy, and ponders the apparent contradiction of human civilization never having encountered any. A well-known attempt to ponder this paradox through the lens of a Fermi estimate is the Drake equation, which seeks to estimate the number of such civilizations present in the galaxy.


== Advantages and scope ==

Scientists often look for Fermi estimates of the answer to a problem before turning to more sophisticated methods to calculate a precise answer. This provides a useful check on the results. While the estimate is almost certainly incorrect, it is also a simple calculation that allows for easy error checking, and to find faulty assumptions if the figure produced is far beyond what we might reasonably expect. By contrast, precise calculations can be extremely complex but with the expectation that the answer they produce is correct. The far larger number of factors and operations involved can obscure a very significant error, either in mathematical process or in the assumptions the equation is based on, but the result may still be assumed to be right because it has been derived from a precise formula that is expected to yield good results. Without a reasonable frame of reference to work from it is seldom clear if a result is acceptably precise or is many degrees of magnitude (tens or hundreds of times) too big or too small. The Fermi estimation gives a quick, simple way to obtain this frame of reference for what might reasonably be expected to be the answer.
As long as the initial assumptions in the estimate are reasonable quantities, the result obtained will give an answer within the same scale as the correct result, and if not gives a base for understanding why this is the case. For example, suppose a person was asked to determine the number of piano tuners in Chicago. 
If their initial estimate told them there should be a hundred or so, but the precise answer tells them there are many thousands, then they know they need to find out why there is this divergence from the expected result. First looking for errors, then for factors the estimation did not take account of – does Chicago have a number of music schools or other places with a disproportionately high ratio of pianos to people? Whether close or very far from the observed results, the context the estimation provides gives useful information both about the process of calculation and the assumptions that have been used to look at problems.
Fermi estimates are also useful in approaching problems where the optimal choice of calculation method depends on the expected size of the answer. For instance, a Fermi estimate might indicate whether the internal stresses of a structure are low enough that it can be accurately described by linear elasticity; or if the estimate already bears significant relationship in scale relative to some other value, for example, if a structure will be over-engineered to withstand loads several times greater than the estimate.
Although Fermi calculations are often not accurate, as there may be many problems with their assumptions, this sort of analysis does inform one what to look for to get a better answer. For the above example, one might try to find a better estimate of the number of pianos tuned by a piano tuner in a typical day, or look up an accurate number for the population of Chicago.""",
    tier=7,
    domain="arithmetic",
    source="Wikipedia, 'Fermi problem'",
    source_url="https://en.wikipedia.org/wiki/Fermi_problem",
))

register_atom(Atom(
    atom_type="methodology",
    name="derive_formula",
    content="""A mathematical proof is a deductive argument for a mathematical statement, showing that the stated assumptions logically guarantee the conclusion. The argument may use other previously established statements, such as theorems; but every proof can, in principle, be constructed using only certain basic or original assumptions known as axioms, along with the accepted rules of inference. Proofs are examples of exhaustive deductive reasoning that establish logical certainty, to be distinguished from empirical arguments or non-exhaustive inductive reasoning that establish "reasonable expectation". Presenting many cases in which the statement holds is not enough for a proof, which must demonstrate that the statement is true in all possible cases. A proposition that has not been proved but is believed to be true is known as a conjecture, or a hypothesis if frequently used as an assumption for further mathematical work.
Proofs employ logic expressed in mathematical symbols, along with natural language that usually admits some ambiguity. In most mathematical literature, proofs are written in terms of rigorous informal logic. Purely formal proofs, written fully in symbolic language without the involvement of natural language, are considered in proof theory. The distinction between formal and informal proofs has led to much examination of current and historical mathematical practice, quasi-empiricism in mathematics, and so-called folk mathematics, oral traditions in the mainstream mathematical community or in other cultures. The philosophy of mathematics is concerned with the role of language and logic in proofs, and mathematics as a language.


== History and etymology ==

The word proof derives from the Latin probare 'to test'; related words include English probe, probation, and probability, as well as Spanish probar 'to taste' (sometimes 'to touch' or 'to test'), Italian provare 'to try', and German probieren 'to try'. The legal term probity means authority or credibility, the power of testimony to prove facts when given by persons of reputation or status.
Plausibility arguments using heuristic devices such as pictures and analogies preceded strict mathematical proof. It is likely that the idea of demonstrating a conclusion first arose in connection with geometry, which originated in practical problems of land measurement. The development of mathematical proof is primarily the product of ancient Greek mathematics. Thales (624–546 BCE) and Hippocrates of Chios (c. 470–410 BCE) gave some of the first known proofs of theorems in geometry. Eudoxus (408–355 BCE) and Theaetetus (417–369 BCE) formulated theorems but did not prove them. Aristotle (384–322 BCE) said definitions should describe the concept being defined in terms of other concepts already known.
Mathematical proof was revolutionized by Euclid (300 BCE), who introduced the axiomatic method still in use today. It starts with undefined terms and axioms, propositions concerning the undefined terms which are assumed to be self-evidently true (from Greek axios 'something worthy'). From this basis, the method proves theorems using deductive logic. Euclid's Elements was read by anyone who was considered educated in the West until the middle of the 20th century. In addition to theorems of geometry, such as the Pythagorean theorem, the Elements also covers number theory, including a proof that the square root of two is irrational and a proof that there are infinitely many prime numbers.
Further advances also took place in medieval Islamic mathematics. In the 10th century, the Iraqi mathematician Al-Hashimi worked with numbers as such, called "lines" but not necessarily considered as measurements of geometric objects, to prove algebraic propositions concerning multiplication, division, etc., including the existence of irrational numbers. An inductive proof for arithmetic progressions was introduced in the Al-Fakhri (1000) by Al-Karaji, who used it to prove the binomial theorem and properties of Pascal's triangle.
Modern proof theory treats proofs as inductively defined data structures, not requiring an assumption that axioms are "true" in any sense. This allows parallel mathematical theories as formal models of a given intuitive concept, based on alternate sets of axioms, for example axiomatic set theory and non-Euclidean geometry.


== Nature and purpose ==
As practiced, a proof is expressed in natural language and is a rigorous argument intended to convince the audience of the truth of a statement. The standard of rigor is not absolute and has varied throughout history. A proof can be presented differently depending on the intended audience. To gain acceptance, a proof has to meet communal standards of rigor; an argument considered vague or incomplete may be rejected.
The concept of proof is formalized in the field of mathematical logic. A formal proof is written in a formal language instead of natural language. A formal proof is a sequence of formulas in a formal language, starting with an assumption, and with each subsequent formula a logical consequence of the preceding ones. This definition makes the concept of proof amenable to study. Indeed, the field of proof theory studies formal proofs and their properties, the most famous and surprising being that almost all axiomatic systems can generate certain undecidable statements not provable within the system.
The definition of a formal proof is intended to capture the concept of proofs as written in the practice of mathematics. The soundness of this definition amounts to the belief that a published proof can, in principle, be converted into a formal proof. However, outside the field of automated proof assistants, this is rarely done in practice. A classic question in philosophy asks whether mathematical proofs are analytic or synthetic. Kant, who introduced the analytic–synthetic distinction, believed mathematical proofs are synthetic, whereas Quine argued in his 1951 "Two Dogmas of Empiricism" that such a distinction is untenable.
Proofs may be admired for their mathematical beauty. The mathematician Paul Erdős was known for describing proofs which he found to be particularly elegant as coming from "The Book", a hypothetical tome containing the most beautiful method(s) of proving each theorem. The book Proofs from THE BOOK, published in 2003, is devoted to presenting 32 proofs its editors find particularly pleasing.


== Methods of proof ==


=== Direct proof ===

In direct proof, the conclusion is established by logically combining the axioms, definitions, and earlier theorems. For example, direct proof can be used to prove that the sum of two even integers is always even:

Consider two even integers x and y. Since they are even, they can be written as x = 2a and y = 2b, respectively, for some integers a and b. Then the sum is x + y = 2a + 2b = 2(a + b). Therefore x + y has 2 as a factor and, by definition, is even. Hence, the sum of any two even integers is even.
This proof uses the definition of even integers, the integer properties of closure under addition and multiplication, and the distributive property.


=== Proof by mathematical induction ===

Despite its name, mathematical induction is a method of deduction, not a form of inductive reasoning. In proof by mathematical induction, a single "base case" is proved, and an "induction rule" is proved that establishes that any arbitrary case implies the next case. Since in principle the induction rule can be applied repeatedly (starting from the proven base case), it follows that all (usually infinitely many) cases are provable. This avoids having to prove each case individually.""",
    tier=7,
    domain="algebra",
    source="Wikipedia, 'Mathematical proof'",
    source_url="https://en.wikipedia.org/wiki/Mathematical_proof",
))

register_atom(Atom(
    atom_type="principle",
    name="sufficiency_analysis",
    content="""In statistics, sufficiency is a property of a statistic computed on a sample dataset in relation to a parametric model of the dataset. A sufficient statistic for a model parameter contains all of the information that the dataset provides about that parameter. It is closely related to the concepts of an ancillary statistic which contains no information about the model parameters, and of a complete statistic which only contains information about the parameters and no ancillary information.
A related concept is that of linear sufficiency, which is weaker than sufficiency but can be applied in some cases where there is no sufficient statistic, although it is restricted to linear estimators. The Kolmogorov structure function deals with individual finite data; the related notion there is the algorithmic sufficient statistic.
The concept is due to Sir Ronald Fisher in 1920. Stephen Stigler noted in 1973 that the concept of sufficiency had fallen out of favor in descriptive statistics because of the strong dependence on an assumption of the distributional form (see Pitman–Koopman–Darmois theorem below), but remained very important in theoretical work.


== Background ==
Roughly, given a set 
  
    
      
        
          X
        
      
    
    {\\displaystyle \\mathbf {X} }
  
 of independent identically distributed data conditioned on an unknown parameter 
  
    
      
        θ
      
    
    {\\displaystyle \\theta }
  
, a sufficient statistic is a function 
  
    
      
        T
        (
        
          X
        
        )
      
    
    {\\displaystyle T(\\mathbf {X} )}
  
 whose value contains all the information needed to compute any estimate of the parameter (e.g. a maximum likelihood estimate).  Due to the factorization theorem (see below), for a sufficient statistic 
  
    
      
        T
        (
        
          X
        
        )
      
    
    {\\displaystyle T(\\mathbf {X} )}
  
, the probability density can be written as 
  
    
      
        
          f
          
            
              X
            
          
        
        (
        x
        ;
        θ
        )
        =
        h
        (
        x
        )
        
        g
        (
        θ
        ,
        T
        (
        x
        )
        )
      
    
    {\\displaystyle f_{\\mathbf {X} }(x;\\theta )=h(x)\\,g(\\theta ,T(x))}
  
.  From this factorization, it can easily be seen that the maximum likelihood estimate of 
  
    
      
        θ
      
    
    {\\displaystyle \\theta }
  
 will interact with 
  
    
      
        
          X
        
      
    
    {\\displaystyle \\mathbf {X} }
  
 only through 
  
    
      
        T
        (
        
          X
        
        )
      
    
    {\\displaystyle T(\\mathbf {X} )}
  
.  Typically, the sufficient statistic is a simple function of the data, e.g. the sum of all the data points.
More generally, the "unknown parameter" may represent a vector of unknown quantities or may represent everything about the model that is unknown or not fully specified.  In such a case, the sufficient statistic may be a set of functions, called a jointly sufficient statistic.  Typically, there are as many functions as there are parameters.  For example, for a Gaussian distribution with unknown mean and variance, the jointly sufficient statistic, from which maximum likelihood estimates of both parameters can be estimated, consists of two functions, the sum of all data points and the sum of all squared data points (or equivalently, the sample mean and sample variance).
In other words, the joint probability distribution of the data is conditionally independent of the parameter given the value of the sufficient statistic for the parameter. Both the statistic and the underlying parameter can be vectors.


== Mathematical definition ==
A statistic t = T(X) is sufficient for underlying parameter θ precisely if the conditional probability distribution of the data X, given the statistic t = T(X), does not depend on the  parameter θ.
Alternatively, one can say the statistic T(X) is sufficient for θ if, for all prior distributions on θ, the mutual information between θ and T(X) equals the mutual information between θ and X. In other words, the data processing inequality becomes an equality:

  
    
      
        I
        
          
            (
          
        
        θ
        ;
        T
        (
        X
        )
        
          
            )
          
        
        =
        I
        (
        θ
        ;
        X
        )
      
    
    {\\displaystyle I{\\bigl (}\\theta ;T(X){\\bigr )}=I(\\theta ;X)}
  


=== Example ===
As an example, the sample mean is sufficient for the (unknown) mean μ of a normal distribution with known variance. Once the sample mean is known, no further information about μ can be obtained from the sample itself.  On the other hand, for an arbitrary distribution the median is not sufficient for the mean: even if the median of the sample is known, knowing the sample itself would provide further information about the population mean.  For example, if the observations that are less than the median are only slightly less, but observations exceeding the median exceed it by a large amount, then this would have a bearing on one's inference about the population mean.


== Fisher–Neyman factorization theorem ==
Fisher's factorization theorem or factorization criterion provides a convenient characterization of a sufficient statistic.  If the probability density function is ƒθ(x), then T is sufficient for θ if and only if nonnegative functions g and h can be found such that

  
    
      
        f
        (
        x
        ;
        θ
        )
        =
        h
        (
        x
        )
        
        g
        (
        θ
        ,
        T
        (
        x
        )
        )
        ,
      
    
    {\\displaystyle f(x;\\theta )=h(x)\\,g(\\theta ,T(x)),}
  

i.e., the density ƒ can be factored into a product such that one factor, h, does not depend on θ and the other factor, which does depend on θ, depends on x only through T(x). A general proof of this was given by Halmos and Savage and the theorem is sometimes referred to as the Halmos–Savage factorization theorem. The proofs below handle special cases, but an alternative general proof along the same lines can be given. In many simple cases the probability density function is fully specified by 
  
    
      
        θ
      
    
    {\\displaystyle \\theta }
  
 and 
  
    
      
        T
        (
        x
        )
      
    
    {\\displaystyle T(x)}
  
, and 
  
    
      
        h
        (
        x
        )
        =
        1
      
    
    {\\displaystyle h(x)=1}
  
 (see Examples). 
It is easy to see that if F(t) is a one-to-one function and T is a sufficient
statistic, then F(T) is a sufficient statistic. In particular we can multiply a
sufficient statistic by a nonzero constant and get another sufficient statistic.


=== Likelihood principle interpretation ===
An implication of the theorem is that when using likelihood-based inference, two sets of data yielding the same value for the sufficient statistic T(X) will always yield the same inferences about θ.  By the factorization criterion, the likelihood's dependence on θ is only in conjunction with T(X).  As this is the same in both cases, the dependence on θ will be the same as well, leading to identical inferences.


=== Proof ===
Due to Hogg and Craig. Let 
  
    
      
        
          X
          
            1
          
        
        ,
        
          X
          
            2
          
        
        ,
        …
        ,
        
          X
          
            n
          
        
      
    
    {\\displaystyle X_{1},X_{2},\\ldots ,X_{n}}
  
,  denote a random sample from a distribution having the pdf f(x, θ) for ι < θ < δ. Let Y1 = u1(X1, X2, ..., Xn) be a statistic whose pdf is g1(y1; θ).""",
    tier=7,
    domain="algebra",
    source="Wikipedia, 'Sufficient statistic'",
    source_url="https://en.wikipedia.org/wiki/Sufficient_statistic",
))

register_atom(Atom(
    atom_type="principle",
    name="isomorphism_detection",
    content="""In mathematics, an isomorphism is a structure-preserving mapping or morphism between two structures of the same type that can be reversed by an inverse mapping. Two mathematical structures are isomorphic if an isomorphism exists between them, and this is often denoted as ⁠
  
    
      
        A
        ≅
        B
      
    
    {\\displaystyle A\\cong B}
  
⁠. The word is derived from Ancient Greek  ἴσος (isos) 'equal' and  μορφή (morphe) 'form, shape'.
The interest in isomorphisms lies in the fact that two isomorphic objects have the same properties (excluding further information such as additional structure or names of objects). Thus isomorphic structures cannot be distinguished from the point of view of structure only, and may often be identified. In mathematical jargon, one says that two objects are the same up to an isomorphism. A common example where isomorphic structures cannot be identified is when the structures are substructures of a larger one. For example, all subspaces of dimension one of a vector space are isomorphic and cannot be identified.
An automorphism is an isomorphism from a structure to itself. An isomorphism between two structures is a canonical isomorphism  (a canonical map that is an isomorphism) if there is only one isomorphism between the two structures (as is the case for solutions of a universal property), or if the isomorphism is much more natural (in some sense) than other isomorphisms. For example, for every prime number p, all fields with p elements are canonically isomorphic, with a unique isomorphism. The isomorphism theorems provide canonical isomorphisms that are not unique.
The term isomorphism is mainly used for algebraic structures and categories. In the case of algebraic structures, mappings are called homomorphisms, and a homomorphism is an isomorphism if and only if it is bijective. 
In various areas of mathematics, isomorphisms have received specialized names, depending on the type of structure under consideration. For example:

An isometry is an isomorphism of metric spaces.
A homeomorphism is an isomorphism of topological spaces.
A diffeomorphism is an isomorphism of spaces equipped with a differential structure, typically differentiable manifolds.
A symplectomorphism is an isomorphism of symplectic manifolds.
A permutation is an automorphism of a set.
In geometry, isomorphisms and automorphisms are often called transformations, for example rigid transformations, affine transformations, projective transformations.
Category theory, which can be viewed as a formalization of the concept of mapping between structures, provides a language that may be used to unify the approach to these different aspects of the basic idea.


== Examples ==


=== Logarithm and exponential ===
Let 
  
    
      
        
          
            R
          
          
            +
          
        
      
    
    {\\displaystyle \\mathbb {R} ^{+}}
  
 be the multiplicative group of positive real numbers, and let 
  
    
      
        
          R
        
      
    
    {\\displaystyle \\mathbb {R} }
  
 be the additive group of real numbers.
The logarithm function 
  
    
      
        log
        :
        
          
            R
          
          
            +
          
        
        →
        
          R
        
      
    
    {\\displaystyle \\log :\\mathbb {R} ^{+}\\to \\mathbb {R} }
  
 satisfies 
  
    
      
        log
        ⁡
        (
        x
        y
        )
        =
        log
        ⁡
        x
        +
        log
        ⁡
        y
      
    
    {\\displaystyle \\log(xy)=\\log x+\\log y}
  
 for all 
  
    
      
        x
        ,
        y
        ∈
        
          
            R
          
          
            +
          
        
        ,
      
    
    {\\displaystyle x,y\\in \\mathbb {R} ^{+},}
  
 so it is a group homomorphism. The exponential function 
  
    
      
        exp
        :
        
          R
        
        →
        
          
            R
          
          
            +
          
        
      
    
    {\\displaystyle \\exp :\\mathbb {R} \\to \\mathbb {R} ^{+}}
  
 satisfies 
  
    
      
        exp
        ⁡
        (
        x
        +
        y
        )
        =
        (
        exp
        ⁡
        x
        )
        (
        exp
        ⁡
        y
        )
      
    
    {\\displaystyle \\exp(x+y)=(\\exp x)(\\exp y)}
  
 for all 
  
    
      
        x
        ,
        y
        ∈
        
          R
        
        ,
      
    
    {\\displaystyle x,y\\in \\mathbb {R} ,}
  
 so it too is a homomorphism.
The identities 
  
    
      
        log
        ⁡
        exp
        ⁡
        x
        =
        x
      
    
    {\\displaystyle \\log \\exp x=x}
  
 and 
  
    
      
        exp
        ⁡
        log
        ⁡
        y
        =
        y
      
    
    {\\displaystyle \\exp \\log y=y}
  
 show that 
  
    
      
        log
      
    
    {\\displaystyle \\log }
  
 and 
  
    
      
        exp
      
    
    {\\displaystyle \\exp }
  
 are inverses of each other. So,

  
    
      
        exp
        :
        
          R
        
        →
        
          
            R
          
          
            +
          
        
        
        
          and
        
        
        log
        :
        
          
            R
          
          
            +
          
        
        →
        
          R
        
      
    
    {\\displaystyle \\exp :\\mathbb {R} \\to \\mathbb {R} ^{+}\\quad {\\text{and}}\\quad \\log :\\mathbb {R} ^{+}\\to \\mathbb {R} }
  

are group isomorphisms that are inverse of each other.
The 
  
    
      
        log
      
    
    {\\displaystyle \\log }
  
 function is an isomorphism which translates multiplication of positive real numbers into addition of real numbers. This facility makes it possible to multiply real numbers using a ruler and a table of logarithms, or using a slide rule with a logarithmic scale.


=== Integers modulo 6 ===
Consider the ring 
  
    
      
        
          
            Z
          
          
            6
          
        
      
    
    {\\displaystyle \\mathbb {Z} _{6}}
  
 of the integers from 0 to 5 with addition and multiplication modulo 6.""",
    tier=8,
    domain="abstract_algebra",
    source="Wikipedia, 'Isomorphism'",
    source_url="https://en.wikipedia.org/wiki/Isomorphism",
))

register_atom(Atom(
    atom_type="principle",
    name="cross_domain_transfer",
    content="""Transfer learning (TL) is a technique in machine learning (ML) in which knowledge learned from a task is re-used in order to boost performance on a related task. For example, for image classification, knowledge gained while learning to recognize cars could be applied when trying to recognize trucks. This topic is related to the psychological literature on transfer of learning, although practical ties between the two fields are limited. Reusing or transferring information from previously learned tasks to new tasks has the potential to significantly improve learning efficiency.
Since transfer learning makes use of training with multiple objective functions it is related to cost-sensitive machine learning and multi-objective optimization.


== History ==
In 1976, Bozinovski and Fulgosi published a paper addressing transfer learning in neural network training. The paper gives a mathematical and geometrical model of the topic. In 1981, a report considered the application of transfer learning to a dataset of images representing letters of computer terminals, experimentally demonstrating positive and negative transfer learning.
In 1992, Lorien Pratt formulated the discriminability-based transfer (DBT) algorithm.
By 1998, the field had advanced to include multi-task learning, along with more formal theoretical foundations. Influential publications on transfer learning include the book Learning to Learn in 1998, a 2009 survey and a 2019 survey.
Ng said in his NIPS 2016 tutorial that TL would become the next driver of machine learning commercial success after supervised learning.
In the 2020 paper, "Rethinking Pre-Training and self-training", Zoph et al. reported that pre-training can hurt accuracy, and advocate self-training instead.


== Definition ==
The definition of transfer learning is given in terms of domains and tasks. A domain 
  
    
      
        
          
            D
          
        
      
    
    {\\displaystyle {\\mathcal {D}}}
  
 consists of: a feature space 
  
    
      
        
          
            X
          
        
      
    
    {\\displaystyle {\\mathcal {X}}}
  
 and a marginal probability distribution 
  
    
      
        P
        (
        X
        )
      
    
    {\\displaystyle P(X)}
  
, where 
  
    
      
        X
        =
        {
        
          x
          
            1
          
        
        ,
        .
        .
        .
        ,
        
          x
          
            n
          
        
        }
        ∈
        
          
            X
          
        
      
    
    {\\displaystyle X=\\{x_{1},...,x_{n}\\}\\in {\\mathcal {X}}}
  
. Given a specific domain, 
  
    
      
        
          
            D
          
        
        =
        {
        
          
            X
          
        
        ,
        P
        (
        X
        )
        }
      
    
    {\\displaystyle {\\mathcal {D}}=\\{{\\mathcal {X}},P(X)\\}}
  
, a task consists of two components: a label space 
  
    
      
        
          
            Y
          
        
      
    
    {\\displaystyle {\\mathcal {Y}}}
  
 and an objective predictive function 
  
    
      
        f
        :
        
          
            X
          
        
        →
        
          
            Y
          
        
      
    
    {\\displaystyle f:{\\mathcal {X}}\\rightarrow {\\mathcal {Y}}}
  
. The function 
  
    
      
        f
      
    
    {\\displaystyle f}
  
 is used to predict the corresponding label 
  
    
      
        f
        (
        x
        )
      
    
    {\\displaystyle f(x)}
  
 of a new instance 
  
    
      
        x
      
    
    {\\displaystyle x}
  
. This task, denoted by 
  
    
      
        
          
            T
          
        
        =
        {
        
          
            Y
          
        
        ,
        f
        (
        x
        )
        }
      
    
    {\\displaystyle {\\mathcal {T}}=\\{{\\mathcal {Y}},f(x)\\}}
  
, is learned from the training data consisting of pairs 
  
    
      
        {
        
          x
          
            i
          
        
        ,
        
          y
          
            i
          
        
        }
      
    
    {\\displaystyle \\{x_{i},y_{i}\\}}
  
, where 
  
    
      
        
          x
          
            i
          
        
        ∈
        
          
            X
          
        
      
    
    {\\displaystyle x_{i}\\in {\\mathcal {X}}}
  
 and 
  
    
      
        
          y
          
            i
          
        
        ∈
        
          
            Y
          
        
      
    
    {\\displaystyle y_{i}\\in {\\mathcal {Y}}}
  
.
Given a source domain 
  
    
      
        
          
            
              D
            
          
          
            S
          
        
      
    
    {\\displaystyle {\\mathcal {D}}_{S}}
  
 and learning task 
  
    
      
        
          
            
              T
            
          
          
            S
          
        
      
    
    {\\displaystyle {\\mathcal {T}}_{S}}
  
, a target domain 
  
    
      
        
          
            
              D
            
          
          
            T
          
        
      
    
    {\\displaystyle {\\mathcal {D}}_{T}}
  
 and learning task 
  
    
      
        
          
            
              T
            
          
          
            T
          
        
      
    
    {\\displaystyle {\\mathcal {T}}_{T}}
  
, where 
  
    
      
        
          
            
              D
            
          
          
            S
          
        
        ≠
        
          
            
              D
            
          
          
            T
          
        
      
    
    {\\displaystyle {\\mathcal {D}}_{S}\\neq {\\mathcal {D}}_{T}}
  
, or 
  
    
      
        
          
            
              T
            
          
          
            S
          
        
        ≠
        
          
            
              T
            
          
          
            T
          
        
      
    
    {\\displaystyle {\\mathcal {T}}_{S}\\neq {\\mathcal {T}}_{T}}
  
, transfer learning aims to help improve the learning of the target predictive function 
  
    
      
        
          f
          
            T
          
        
        (
        ⋅
        )
      
    
    {\\displaystyle f_{T}(\\cdot )}
  
 in 
  
    
      
        
          
            
              D
            
          
          
            T
          
        
      
    
    {\\displaystyle {\\mathcal {D}}_{T}}
  
 using the knowledge in 
  
    
      
        
          
            
              D
            
          
          
            S
          
        
      
    
    {\\displaystyle {\\mathcal {D}}_{S}}
  
 and 
  
    
      
        
          
            
              T
            
          
          
            S
          
        
      
    
    {\\displaystyle {\\mathcal {T}}_{S}}
  
.


== Applications ==
Algorithms for transfer learning are available in Markov logic networks and Bayesian networks. Transfer learning has been applied to cancer subtype discovery, building utilization, general game playing, text classification, digit recognition, medical imaging and spam filtering.
In 2020, it was discovered that, due to their similar physical natures, transfer learning is possible between electromyographic (EMG) signals from the muscles and classifying the behaviors of electroencephalographic (EEG) brainwaves, from the gesture recognition domain to the mental state recognition domain. It was noted that this relationship worked in both directions, showing that electroencephalographic can likewise be used to classify EMG.""",
    tier=8,
    domain="methodology",
    source="Wikipedia, 'Transfer learning'",
    source_url="https://en.wikipedia.org/wiki/Transfer_learning",
))

register_atom(Atom(
    atom_type="methodology",
    name="conjecture_generation",
    content="""In mathematics, a conjecture is a proposition that is proffered on a tentative basis without proof. Some conjectures, such as the Riemann hypothesis or Fermat's conjecture (now a theorem, proven in 1995 by Andrew Wiles), have shaped much of mathematical history as new areas of mathematics are developed in order to prove them.


== Resolution of conjectures ==


=== Proof ===
Formal mathematics is based on provable truth. In mathematics, any number of cases supporting a universally quantified conjecture, no matter how large, is insufficient for establishing the conjecture's veracity, since a single counterexample could immediately bring down the conjecture. Mathematical journals sometimes publish the minor results of research teams having extended the search for a counterexample farther than previously done. For instance, the Collatz conjecture, which concerns whether or not certain sequences of integers terminate, has been tested for all integers up to 1.2 × 1012 (1.2 trillion). However, the failure to find a counterexample after extensive search does not constitute a proof that the conjecture is true—because the conjecture might be false but with a very large minimal counterexample.
Nevertheless, mathematicians often regard a conjecture as strongly supported by evidence even though not yet proved. That evidence may be of various kinds, such as verification of consequences of it or strong interconnections with known results.
A conjecture is considered proven only when it has been shown that it is logically impossible for it to be false. There are various methods of doing so; see methods of mathematical proof for more details.
One method of proof, applicable when there are only a finite number of cases that could lead to counterexamples, is known as "brute force": in this approach, all possible cases are considered and shown not to give counterexamples. In some occasions, the number of cases is quite large, in which case a brute-force proof may require as a practical matter the use of a computer algorithm to check all the cases. For example, the validity of the 1976 and 1997 brute-force proofs of the four color theorem by computer was initially doubted, but was eventually confirmed in 2005 by theorem-proving software.
When a conjecture has been proven, it is no longer a conjecture but a theorem. Many important theorems were once conjectures, such as the Geometrization theorem (which resolved the Poincaré conjecture), Fermat's Last Theorem, and others.


=== Disproof ===
Conjectures disproven through counterexample are sometimes referred to as false conjectures (cf. the Pólya conjecture and Euler's sum of powers conjecture). In the case of the latter, the first counterexample found for the n=4 case involved numbers in the millions, although it has been subsequently found that the minimal counterexample is actually smaller.


=== Independent conjectures ===
Not every conjecture ends up being proven true or false. The continuum hypothesis, which tries to ascertain the relative cardinality of certain infinite sets, was eventually shown to be independent from the generally accepted set of Zermelo–Fraenkel axioms of set theory. It is therefore possible to adopt this statement, or its negation, as a new axiom in a consistent manner (much as Euclid's parallel postulate can be taken either as true or false in an axiomatic system for geometry).
In this case, if a proof uses this statement, researchers will often look for a new proof that does not require the hypothesis (in the same way that it is desirable that statements in Euclidean geometry be proved using only the axioms of neutral geometry, i.e. without the parallel postulate). The one major exception to this in practice is the axiom of choice, as the majority of researchers usually do not worry whether a result requires it—unless they are studying this axiom in particular.


== Conditional proofs ==
Sometimes, a conjecture is called a hypothesis when it is used frequently and repeatedly as an assumption in proofs of other results. For example, the Riemann hypothesis is a conjecture from number theory that — amongst other things — makes predictions about the distribution of prime numbers. Few number theorists doubt that the Riemann hypothesis is true. In fact, in anticipation of its eventual proof, some have even proceeded to develop further proofs which are contingent on the truth of this conjecture. These are called conditional proofs: the conjectures assumed appear in the hypotheses of the theorem, for the time being.
These "proofs", however, would fall apart if it turned out that the hypothesis was false, so there is considerable interest in verifying the truth or falsity of conjectures of this type.


== Important examples ==


=== Fermat's Last Theorem ===

In number theory, Fermat's Last Theorem (sometimes called Fermat's conjecture, especially in older texts) states that no three positive integers 
  
    
      
        a
      
    
    {\\displaystyle a}
  
, 
  
    
      
        b
      
    
    {\\displaystyle b}
  
, and 
  
    
      
        c
      
    
    {\\displaystyle c}
  
 can satisfy the equation 
  
    
      
        
          a
          
            n
          
        
        +
        
          b
          
            n
          
        
        =
        
          c
          
            n
          
        
      
    
    {\\displaystyle a^{n}+b^{n}=c^{n}}
  
 for any integer value of 
  
    
      
        n
      
    
    {\\displaystyle n}
  
 greater than two.
This theorem was first conjectured by Pierre de Fermat in 1637 in the margin of a copy of Arithmetica, where he claimed that he had a proof that was too large to fit in the margin. The first successful proof was released in 1994 by Andrew Wiles, and formally published in 1995, after 358 years of effort by mathematicians. The unsolved problem stimulated the development of algebraic number theory in the 19th century, and the proof of the modularity theorem in the 20th century. It is among the most notable theorems in the history of mathematics, and prior to its proof it was in the Guinness Book of World Records for "most difficult mathematical problems".


=== Four color theorem ===

In mathematics, the four color theorem, or the four color map theorem, states that given any separation of a plane into contiguous regions, producing a figure called a map, no more than four colors are required to color the regions of the map—so that no two adjacent regions have the same color. Two regions are called adjacent if they share a common boundary that is not a corner, where corners are the points shared by three or more regions. For example, in the map of the United States of America, Utah and Arizona are adjacent, but Utah and New Mexico, which only share a point that also belongs to Arizona and Colorado, are not.
Möbius mentioned the problem in his lectures as early as 1840. The conjecture was first proposed on October 23, 1852 when Francis Guthrie, while trying to color the map of counties of England, noticed that only four different colors were needed. The five color theorem, which has a short elementary proof, states that five colors suffice to color a map and was proven in the late 19th century; however, proving that four colors suffice turned out to be significantly harder. A number of false proofs and false counterexamples have appeared since the first statement of the four color theorem in 1852.
The four color theorem was ultimately proven in 1976 by Kenneth Appel and Wolfgang Haken. It was the first major theorem to be proved using a computer. Appel and Haken's approach started by showing that there is a particular set of 1,936 maps, each of which cannot be part of a smallest-sized counterexample to the four color theorem (i.e., if they did appear, one could make a smaller counter-example). Appel and Haken used a special-purpose computer program to confirm that each of these maps had this property.""",
    tier=8,
    domain="methodology",
    source="Wikipedia, 'Conjecture'",
    source_url="https://en.wikipedia.org/wiki/Conjecture",
))

register_atom(Atom(
    atom_type="principle",
    name="complexity_reduction",
    content="""In computability theory and computational complexity theory, a reduction is an algorithm for transforming one problem into another problem. A sufficiently efficient reduction from one problem to another may be used to show that the second problem is at least as difficult as the first.
Intuitively, problem A is reducible to problem B, if an algorithm for solving problem B efficiently (if it exists) could also be used as a subroutine to solve problem A efficiently. When this is true, solving A cannot be harder than solving B. "Harder" means having a higher estimate of the required computational resources in a given context (e.g., higher time complexity, greater memory requirement, need for extra hardware processor cores for a parallel solution compared to a single-threaded solution, etc.). The existence of a reduction from A to B can be written in the shorthand notation A ≤m B, usually with a subscript on the ≤ to indicate the type of reduction being used (m : many-one reduction, p : polynomial reduction).
The mathematical structure generated on a set of problems by the reductions of a particular type generally forms a preorder, whose equivalence classes may be used to define degrees of unsolvability and complexity classes.


== Introduction ==
There are two main situations where we need to use reductions:

First, we find ourselves trying to solve a problem that is similar to a problem we've already solved. In these cases, often a quick way of solving the new problem is to transform each instance of the new problem into instances of the old problem, solve these using our existing solution, and then use these to obtain our final solution. This is perhaps the most obvious use of reductions.
Second: suppose we have a problem that we've proven is hard to solve, and we have a similar new problem. We might suspect that it is also hard to solve. We argue by contradiction: suppose the new problem is easy to solve. Then, if we can show that every instance of the old problem can be solved easily by transforming it into instances of the new problem and solving those, we have a contradiction. This establishes that the new problem is also hard.
A very simple example of a reduction is from multiplication to squaring. Suppose all we know how to do is to add, subtract, take squares, and divide by two. We can use this knowledge, combined with the following formula, to obtain the product of any two numbers:

  
    
      
        a
        ×
        b
        =
        
          
            
              (
              
                
                  
                    (
                    
                      a
                      +
                      b
                    
                    )
                  
                  
                    2
                  
                
                −
                
                  a
                  
                    2
                  
                
                −
                
                  b
                  
                    2
                  
                
              
              )
            
            2
          
        
      
    
    {\\displaystyle a\\times b={\\frac {\\left(\\left(a+b\\right)^{2}-a^{2}-b^{2}\\right)}{2}}}
  

We also have a reduction in the other direction; obviously, if we can multiply two numbers, we can square a number. This seems to imply that these two problems are equally hard. This kind of reduction corresponds to Turing reduction.
However, the reduction becomes much harder if we add the restriction that we can only use the squaring function one time, and only at the end. In this case, even if we're allowed to use all the basic arithmetic operations, including multiplication, no reduction exists in general, because in order to get the desired result as a square we have to compute its square root first, and this square root could be an irrational number like 
  
    
      
        
          
            2
          
        
      
    
    {\\displaystyle {\\sqrt {2}}}
  
 that cannot be constructed by arithmetic operations on rational numbers. Going in the other direction, however, we can certainly square a number with just one multiplication, only at the end. Using this limited form of reduction, we have shown the unsurprising result that multiplication is harder in general than squaring. This corresponds to many-one reduction.


== Properties ==
Reducibility is a preordering, that is, a reflexive and transitive relation, on P(N)×P(N), where P(N) is the power set of the natural numbers.


== Types and applications of reductions ==
As described in the example above, there are two main types of reductions used in computational complexity theory, the many-one reduction and the Turing reduction. Many-one reductions map instances of one problem to instances of another; Turing reductions compute the solution to one problem, assuming the other problem is easy to solve. The many-one reduction is a stronger type of Turing reduction, and is more effective at separating problems into distinct complexity classes. However, the increased restrictions on many-one reductions make them more difficult to find.
A problem is complete for a complexity class if every problem in the class reduces to that problem, and it is also in the class itself. In this sense the problem represents the class, since any solution to it can, in combination with the reductions, be used to solve every problem in the class.
However, in order to be useful, reductions must be easy. For example, it's quite possible to reduce a difficult-to-solve NP-complete problem like the boolean satisfiability problem to a trivial problem, like determining if a number equals zero, by having the reduction machine solve the problem in exponential time and output zero only if there is a solution. However, this does not achieve much, because even though we can solve the new problem, performing the reduction is just as hard as solving the old problem. Likewise, a reduction computing a noncomputable function can reduce an undecidable problem to a decidable one. As Michael Sipser points out in Introduction to the Theory of Computation: "The reduction must be easy, relative to the complexity of typical problems in the class [...] If the reduction itself were difficult to compute, an easy solution to the complete problem wouldn't necessarily yield an easy solution to the problems reducing to it."
Therefore, the appropriate notion of reduction depends on the complexity class being studied. When studying the complexity class NP and many harder classes such as the polynomial hierarchy, polynomial-time reductions are used. When studying classes within P such as NC and NL, log-space reductions are used. Reductions are also used in computability theory to show whether problems are or are not solvable by machines at all; in this case, reductions are restricted only to computable functions (for many-one reductions) or oracle machines (for Turing reductions).
In the case of optimization (maximization or minimization) problems, we often think in terms of approximation-preserving reductions. Suppose we have two optimization problems such that instances of one problem can be mapped onto instances of the other, in a way that nearly optimal solutions to instances of the latter problem can be transformed back to yield nearly optimal solutions to the former. This way, if we have an optimization algorithm (or approximation algorithm) that finds near-optimal (or optimal) solutions to instances of problem B, and an efficient approximation-preserving reduction from problem A to problem B, by composition we obtain an optimization algorithm that yields near-optimal solutions to instances of problem A.""",
    tier=8,
    domain="algebra",
    source="Wikipedia, 'Reduction (complexity)'",
    source_url="https://en.wikipedia.org/wiki/Reduction_%28complexity%29",
))

register_atom(Atom(
    atom_type="methodology",
    name="problem_transformation",
    content="""In computability theory and computational complexity theory, a reduction is an algorithm for transforming one problem into another problem. A sufficiently efficient reduction from one problem to another may be used to show that the second problem is at least as difficult as the first.
Intuitively, problem A is reducible to problem B, if an algorithm for solving problem B efficiently (if it exists) could also be used as a subroutine to solve problem A efficiently. When this is true, solving A cannot be harder than solving B. "Harder" means having a higher estimate of the required computational resources in a given context (e.g., higher time complexity, greater memory requirement, need for extra hardware processor cores for a parallel solution compared to a single-threaded solution, etc.). The existence of a reduction from A to B can be written in the shorthand notation A ≤m B, usually with a subscript on the ≤ to indicate the type of reduction being used (m : many-one reduction, p : polynomial reduction).
The mathematical structure generated on a set of problems by the reductions of a particular type generally forms a preorder, whose equivalence classes may be used to define degrees of unsolvability and complexity classes.


== Introduction ==
There are two main situations where we need to use reductions:

First, we find ourselves trying to solve a problem that is similar to a problem we've already solved. In these cases, often a quick way of solving the new problem is to transform each instance of the new problem into instances of the old problem, solve these using our existing solution, and then use these to obtain our final solution. This is perhaps the most obvious use of reductions.
Second: suppose we have a problem that we've proven is hard to solve, and we have a similar new problem. We might suspect that it is also hard to solve. We argue by contradiction: suppose the new problem is easy to solve. Then, if we can show that every instance of the old problem can be solved easily by transforming it into instances of the new problem and solving those, we have a contradiction. This establishes that the new problem is also hard.
A very simple example of a reduction is from multiplication to squaring. Suppose all we know how to do is to add, subtract, take squares, and divide by two. We can use this knowledge, combined with the following formula, to obtain the product of any two numbers:

  
    
      
        a
        ×
        b
        =
        
          
            
              (
              
                
                  
                    (
                    
                      a
                      +
                      b
                    
                    )
                  
                  
                    2
                  
                
                −
                
                  a
                  
                    2
                  
                
                −
                
                  b
                  
                    2
                  
                
              
              )
            
            2
          
        
      
    
    {\\displaystyle a\\times b={\\frac {\\left(\\left(a+b\\right)^{2}-a^{2}-b^{2}\\right)}{2}}}
  

We also have a reduction in the other direction; obviously, if we can multiply two numbers, we can square a number. This seems to imply that these two problems are equally hard. This kind of reduction corresponds to Turing reduction.
However, the reduction becomes much harder if we add the restriction that we can only use the squaring function one time, and only at the end. In this case, even if we're allowed to use all the basic arithmetic operations, including multiplication, no reduction exists in general, because in order to get the desired result as a square we have to compute its square root first, and this square root could be an irrational number like 
  
    
      
        
          
            2
          
        
      
    
    {\\displaystyle {\\sqrt {2}}}
  
 that cannot be constructed by arithmetic operations on rational numbers. Going in the other direction, however, we can certainly square a number with just one multiplication, only at the end. Using this limited form of reduction, we have shown the unsurprising result that multiplication is harder in general than squaring. This corresponds to many-one reduction.


== Properties ==
Reducibility is a preordering, that is, a reflexive and transitive relation, on P(N)×P(N), where P(N) is the power set of the natural numbers.


== Types and applications of reductions ==
As described in the example above, there are two main types of reductions used in computational complexity theory, the many-one reduction and the Turing reduction. Many-one reductions map instances of one problem to instances of another; Turing reductions compute the solution to one problem, assuming the other problem is easy to solve. The many-one reduction is a stronger type of Turing reduction, and is more effective at separating problems into distinct complexity classes. However, the increased restrictions on many-one reductions make them more difficult to find.
A problem is complete for a complexity class if every problem in the class reduces to that problem, and it is also in the class itself. In this sense the problem represents the class, since any solution to it can, in combination with the reductions, be used to solve every problem in the class.
However, in order to be useful, reductions must be easy. For example, it's quite possible to reduce a difficult-to-solve NP-complete problem like the boolean satisfiability problem to a trivial problem, like determining if a number equals zero, by having the reduction machine solve the problem in exponential time and output zero only if there is a solution. However, this does not achieve much, because even though we can solve the new problem, performing the reduction is just as hard as solving the old problem. Likewise, a reduction computing a noncomputable function can reduce an undecidable problem to a decidable one. As Michael Sipser points out in Introduction to the Theory of Computation: "The reduction must be easy, relative to the complexity of typical problems in the class [...] If the reduction itself were difficult to compute, an easy solution to the complete problem wouldn't necessarily yield an easy solution to the problems reducing to it."
Therefore, the appropriate notion of reduction depends on the complexity class being studied. When studying the complexity class NP and many harder classes such as the polynomial hierarchy, polynomial-time reductions are used. When studying classes within P such as NC and NL, log-space reductions are used. Reductions are also used in computability theory to show whether problems are or are not solvable by machines at all; in this case, reductions are restricted only to computable functions (for many-one reductions) or oracle machines (for Turing reductions).
In the case of optimization (maximization or minimization) problems, we often think in terms of approximation-preserving reductions. Suppose we have two optimization problems such that instances of one problem can be mapped onto instances of the other, in a way that nearly optimal solutions to instances of the latter problem can be transformed back to yield nearly optimal solutions to the former. This way, if we have an optimization algorithm (or approximation algorithm) that finds near-optimal (or optimal) solutions to instances of problem B, and an efficient approximation-preserving reduction from problem A to problem B, by composition we obtain an optimization algorithm that yields near-optimal solutions to instances of problem A.""",
    tier=8,
    domain="algebra",
    source="Wikipedia, 'Reduction (complexity)'",
    source_url="https://en.wikipedia.org/wiki/Reduction_%28complexity%29",
))

register_atom(Atom(
    atom_type="principle",
    name="analogy_completion",
    content="""Analogy is a comparison or correspondence between two things (or two groups of things) because of a third element that they are considered to share.
Logically, it is an inference or an argument from one particular to another particular, as opposed to deduction, induction, and abduction. It is also used where at least one of the premises, or the conclusion, is general rather than particular in nature. It has the general form A is to B as C is to D.
In a broader sense, analogical reasoning is a cognitive process of transferring meaning or information of a particular subject (the analog, or source) onto another (the target); and also the linguistic expression corresponding to such a process. The term analogy can also refer to the relation between the source and the target themselves, which is often (though not always) a similarity, as in the biological notion of analogy.

Analogy plays a significant role in human thought processes. It has been argued that analogy lies at "the core of cognition".


== Etymology ==
The English word analogy derives from the Latin analogia, itself derived from the Greek ἀναλογία, "proportion", from ana- "upon, according to" [also "again", "anew"] + logos "ratio" [also "word, speech, reckoning"].


== Models and theories ==
Analogy plays a significant role in problem solving, as well as decision making, argumentation, perception, generalization, memory, creativity, invention, prediction, emotion, explanation, conceptualization and communication. It lies behind basic tasks such as the identification of places, objects and people, for example, in face perception and facial recognition systems. Hofstadter has argued that analogy is "the core of cognition".
An analogy is not a figure of speech but a kind of thought. Specific analogical language uses exemplification, comparisons, metaphors, similes, allegories, and parables, but not metonymy. Phrases like and so on, and the like, as if, and the very word like also rely on an analogical understanding by the receiver of a message including them. Analogy is important not only in ordinary language and common sense (where proverbs and idioms give many examples of its application) but also in science, philosophy, law and the humanities.
The concepts of association, comparison, correspondence, mathematical and morphological homology, homomorphism, iconicity, isomorphism, metaphor, resemblance, and similarity are closely related to analogy. In cognitive linguistics, the notion of conceptual metaphor may be equivalent to that of analogy. Analogy is also a basis for any comparative arguments as well as experiments whose results are transmitted to objects that have been not under examination (e.g., experiments on rats when results are applied to humans).
Analogy has been studied and discussed since classical antiquity by philosophers, scientists, theologists and lawyers. The last few decades have shown a renewed interest in analogy, most notably in cognitive science.


=== Development ===
Archytas, a contemporary of Plato, described three kinds of analogy: mathematical, harmonic, and geometric: the last being the true analogy
Aristotle identified analogy in works such as Metaphysics and Nicomachean Ethics
Roman lawyers used analogical reasoning and the Greek word analogia. 
In Islamic logic, analogical reasoning was used for the process of qiyas in Islamic sharia law and fiqh jurisprudence. 
Medieval lawyers distinguished analogia legis and analogia iuris (see below).
The Middle Ages saw an increased use and theorization of analogy.
In Christian scholastic theology, analogical arguments were accepted in order to explain the attributes of God.
Aquinas made a distinction between equivocal, univocal and analogical terms, the last being those like healthy that have different but related meanings. Not only a person can be "healthy", but also the food that is good for health (see the contemporary distinction between polysemy and homonymy). 
Thomas Cajetan wrote an influential treatise on analogy. In all of these cases, the wide Platonic and Aristotelian notion of analogy was preserved.
Cajetan named several kinds of analogy that had been used but previously unnamed, particularly:

Analogy of attribution (analogia attributionis) or improper proportionality, e.g., "This food is healthy."
Analogy of proportionality (analogia proportionalitatis) or proper proportionality, e.g., "2 is to 1 as 4 is to 2", or "the goodness of humans is relative to their essence as the goodness of God is relative to God's essence."
Metaphor, e.g., steely determination.


=== Identity of relation ===
In ancient Greek the word αναλογια (analogia) originally meant proportionality, in the mathematical sense, and it was indeed sometimes translated to Latin as proportio. Analogy was understood as identity of relation between any two ordered pairs, whether of mathematical nature or not.
Analogy and abstraction are different cognitive processes, and analogy is often an easier one. This analogy is not comparing all the properties between a hand and a foot, but rather comparing the relationship between a hand and its palm to a foot and its sole. While a hand and a foot have many dissimilarities, the analogy focuses on their similarity in having an inner surface.
The same notion of analogy was used in the US-based SAT college admission tests, that included "analogy questions" in the form "A is to B as C is to what?" For example, "Hand is to palm as foot is to ____?" These questions were usually given in the Aristotelian format: HAND : PALM : : FOOT : ____ While most competent English speakers will immediately give the right answer to the analogy question (sole), it is more difficult to identify and describe the exact relation that holds both between pairs such as hand and palm, and between foot and sole. This relation is not apparent in some lexical definitions of palm and sole, where the former is defined as the inner surface of the hand, and the latter as the underside of the foot.
Kant's Critique of Judgment held to this notion of analogy, arguing that there can be exactly the same relation between two completely different objects.


=== Shared abstraction ===

Greek philosophers such as Plato and Aristotle used a wider notion of analogy. They saw analogy as a shared abstraction. Analogous objects did not share necessarily a relation, but also an idea, a pattern, a regularity, an attribute, an effect or a philosophy. These authors also accepted that comparisons, metaphors and "images" (allegories) could be used as arguments, and sometimes they called them analogies. Analogies should also make those abstractions easier to understand and give confidence to those who use them.
James Francis Ross in Portraying Analogy (1982), the first substantive examination of the topic since Cajetan's De Nominum Analogia, demonstrated that analogy is a systematic and universal feature of natural languages, with identifiable and law-like characteristics which explain how the meanings of words in a sentence are interdependent.


=== Special case of induction ===
Ibn Taymiyya, Francis Bacon and later John Stuart Mill argued that analogy is simply a special case of induction. In their view, analogy is an inductive inference from common known attributes to another probable common attribute, which is known about only in the source of the analogy, in the following form:

Premises
a is C, D, E, F, G
b is C, D, E, F
Conclusion
b is probably G.


=== Shared structure ===

Contemporary cognitive scientists use a wide notion of analogy, extensionally close to that of Plato and Aristotle, but framed by Gentner's (1983) structure-mapping theory. The same idea of mapping between source and target is used by conceptual metaphor and conceptual blending theorists. Structure mapping theory concerns both psychology and computer science. According to this view, analogy depends on the mapping or alignment of the elements of source and target.""",
    tier=8,
    domain="reasoning",
    source="Wikipedia, 'Analogy'",
    source_url="https://en.wikipedia.org/wiki/Analogy",
))

register_atom(Atom(
    atom_type="methodology",
    name="equation_construction",
    content="""In numerical analysis, polynomial interpolation is the interpolation of a given data set by the polynomial of lowest possible degree that passes through the points in the dataset.
Given a set of n + 1 data points 
  
    
      
        (
        
          x
          
            0
          
        
        ,
        
          y
          
            0
          
        
        )
        ,
        …
        ,
        (
        
          x
          
            n
          
        
        ,
        
          y
          
            n
          
        
        )
      
    
    {\\displaystyle (x_{0},y_{0}),\\ldots ,(x_{n},y_{n})}
  
, with no two 
  
    
      
        
          x
          
            j
          
        
      
    
    {\\displaystyle x_{j}}
  
 the same, a polynomial function 
  
    
      
        p
        (
        x
        )
        =
        
          a
          
            0
          
        
        +
        
          a
          
            1
          
        
        x
        +
        ⋯
        +
        
          a
          
            n
          
        
        
          x
          
            n
          
        
      
    
    {\\displaystyle p(x)=a_{0}+a_{1}x+\\cdots +a_{n}x^{n}}
  
 is said to interpolate the data if 
  
    
      
        p
        (
        
          x
          
            j
          
        
        )
        =
        
          y
          
            j
          
        
      
    
    {\\displaystyle p(x_{j})=y_{j}}
  
 for each 
  
    
      
        j
        ∈
        {
        0
        ,
        1
        ,
        …
        ,
        n
        }
      
    
    {\\displaystyle j\\in \\{0,1,\\dotsc ,n\\}}
  
.
There is always a unique such polynomial, commonly given by two explicit formulas, the Lagrange polynomials and Newton polynomials.


== Applications ==
The original use of interpolation polynomials was to approximate values of important transcendental functions such as natural logarithm and trigonometric functions. Starting with a few accurately computed data points, the corresponding interpolation polynomial will approximate the function at an arbitrary nearby point. Polynomial interpolation also forms the basis for algorithms in numerical quadrature (Simpson's rule) and numerical ordinary differential equations (multigrid methods).
In computer graphics, polynomials can be used to approximate complicated plane curves given a few specified points, for example the shapes of letters in typography. This is usually done with Bézier curves, which are a simple generalization of interpolation polynomials (having specified tangents as well as specified points).
In numerical analysis, polynomial interpolation is essential to perform sub-quadratic multiplication and squaring, such as Karatsuba multiplication and Toom–Cook multiplication, where interpolation through points on a product polynomial yields the specific product required. For example, given a = f(x) = a0x0 + a1x1 + ··· and b = g(x) = b0x0 + b1x1 + ···, the product ab is a specific value of W(x) = f(x)g(x). One may easily find points along W(x) at small values of x, and interpolation based on those points will yield the terms of W(x) and the specific product ab. As fomulated in Karatsuba multiplication, this technique is substantially faster than quadratic multiplication, even for modest-sized inputs, especially on parallel hardware.
In computer science, polynomial interpolation also leads to algorithms for secure multi party computation and secret sharing.


== Interpolation theorem ==
For any 
  
    
      
        n
        +
        1
      
    
    {\\displaystyle n+1}
  
 bivariate data points 
  
    
      
        (
        
          x
          
            0
          
        
        ,
        
          y
          
            0
          
        
        )
        ,
        …
        ,
        (
        
          x
          
            n
          
        
        ,
        
          y
          
            n
          
        
        )
        ∈
        
          
            R
          
          
            2
          
        
      
    
    {\\displaystyle (x_{0},y_{0}),\\dotsc ,(x_{n},y_{n})\\in \\mathbb {R} ^{2}}
  
, where no two 
  
    
      
        
          x
          
            j
          
        
      
    
    {\\displaystyle x_{j}}
  
 are the same, there exists a unique polynomial 
  
    
      
        p
        (
        x
        )
      
    
    {\\displaystyle p(x)}
  
 of degree at most 
  
    
      
        n
      
    
    {\\displaystyle n}
  
 that interpolates these points, i.e. 
  
    
      
        p
        (
        
          x
          
            0
          
        
        )
        =
        
          y
          
            0
          
        
        ,
        …
        ,
        p
        (
        
          x
          
            n
          
        
        )
        =
        
          y
          
            n
          
        
      
    
    {\\displaystyle p(x_{0})=y_{0},\\ldots ,p(x_{n})=y_{n}}
  
.
Equivalently, for a fixed choice of interpolation nodes 
  
    
      
        
          x
          
            j
          
        
      
    
    {\\displaystyle x_{j}}
  
, polynomial interpolation defines a linear bijection 
  
    
      
        
          L
          
            n
          
        
      
    
    {\\displaystyle L_{n}}
  
 between the (n+1)-tuples of real-number values 
  
    
      
        (
        
          y
          
            0
          
        
        ,
        …
        ,
        
          y
          
            n
          
        
        )
        ∈
        
          
            R
          
          
            n
            +
            1
          
        
      
    
    {\\displaystyle (y_{0},\\ldots ,y_{n})\\in \\mathbb {R} ^{n+1}}
  
 and the vector space 
  
    
      
        P
        (
        n
        )
      
    
    {\\displaystyle P(n)}
  
 of real polynomials of degree at most n:

  
    
      
        
          L
          
            n
          
        
        :
        
          
            R
          
          
            n
            +
            1
          
        
        
          
            
              
                ⟶
              
              
                ∼
              
            
          
        
        
        P
        (
        n
        )
        .
      
    
    {\\displaystyle L_{n}:\\mathbb {R} ^{n+1}{\\stackrel {\\sim }{\\longrightarrow }}\\,P(n).}
  

This is a type of unisolvence theorem.""",
    tier=8,
    domain="algebra",
    source="Wikipedia, 'Polynomial interpolation'",
    source_url="https://en.wikipedia.org/wiki/Polynomial_interpolation",
))

register_atom(Atom(
    atom_type="methodology",
    name="self_evaluation",
    content="""Metacognition is an awareness of one's thought processes and an understanding of the patterns behind them. Is "thinking about thinking". The term comes from the root word meta, meaning "beyond", or "on top of". Metacognition can take many forms, such as reflecting on one's ways of thinking, and knowing when and how oneself and others use particular strategies for problem-solving. There are generally two components of metacognition: (1) cognitive conceptions and (2) a cognitive regulation system. Research has shown that both components of metacognition play key roles in metaconceptual knowledge and learning. Metamemory, defined as knowing about memory and mnemonic strategies, is an important aspect of metacognition.
Writings on metacognition date back at least as far as two works by the Greek philosopher Aristotle (384–322 BC): On the Soul and the Parva Naturalia.


== Definitions ==

This higher-level cognition was given the label metacognition by American developmental psychologist John H. Flavell (1979).
The term metacognition literally means 'above cognition', and is used to indicate cognition about cognition, or more informally, thinking about thinking. Flavell defined metacognition as knowledge about cognition and control of cognition. For example, a person is engaging in metacognition if they notice that they are having more trouble learning A than B, or if it strikes them that they should double-check C before accepting it as fact. J. H. Flavell (1976, p. 232). Andreas Demetriou's theory (one of the neo-Piagetian theories of cognitive development) used the term hyper-cognition to refer to self-monitoring, self-representation, and self-regulation processes, which are regarded as integral components of the human mind. Moreover, with his colleagues, he showed that these processes participate in general intelligence, together with processing efficiency and reasoning, which have traditionally been considered to compose fluid intelligence.
Metacognition also involves thinking about one's own thinking process such as study skills, memory capabilities, and the ability to monitor learning. This concept needs to be explicitly taught along with content instruction. A pithy statement from M.D. Gall et al. is often cited in this respect: "Learning how to learn cannot be left to students. It must be taught." 
Metacognition is a general term encompassing the study of memory-monitoring and self-regulation, meta-reasoning, consciousness/awareness and autonoetic consciousness/self-awareness. In practice these capacities are used to regulate one's own cognition, to maximize one's potential to think, learn and to the evaluation of proper ethical/moral rules. It can also lead to a reduction in response time for a given situation as a result of heightened awareness, and potentially reduce the time to complete problems or tasks.
In the context of student metacognition, D. N. Perkins and Gavriel Salomon observe that metacognition concerns students' ability to monitor their progress. During this process, students ask questions like "What am I doing now?", "Is it getting me anywhere?", and "What else could I be doing instead?". Perkins and Salomon argue that such metacognitive practices help students to avoid unproductive approaches. 
In the domain of experimental psychology, an influential distinction in metacognition (proposed by T. O. Nelson & L. Narens) is between Monitoring—making judgments about the strength of one's memories—and Control—using those judgments to guide behavior (in particular, to guide study choices). Dunlosky, Serra, and Baker (2007) covered this distinction in a review of metamemory research that focused on how findings from this domain can be applied to other areas of applied research.
In the domain of cognitive neuroscience, metacognitive monitoring and control has been viewed as a function of the prefrontal cortex, which receives (monitors) sensory signals from other cortical regions and implements control using feedback loops (see chapters by Schwartz & Bacon and Shimamura, in Dunlosky & Bjork, 2008).
Metacognition is studied in the domain of artificial intelligence and modelling. Therefore, it is the domain of interest of emergent systemics.


== Concepts and models ==
Metacognition has two interacting phenomena guided by a person's cognitive regulation:

Metacognitive knowledge (also called metacognitive awareness) is what individuals know about themselves and others like beliefs about thinking and such, as cognitive processors.
Metacognitive experiences are those experiences that have something to do with the current, on-going cognitive endeavor.
Metacognition refers to a level of thinking and metacognitive regulation, the regulation of cognition and subsequent learning experiences that help people enhance their learning through a set of activities. It involves active metacognitive control or attention over the process in learning situations. The skills that aid in regulation involve planning the way to approach a learning task, monitoring comprehension, and evaluating progress towards the completion of a task.
Metacognition includes at least three different types of metacognitive awareness when considering metacognitive knowledge: 

Declarative knowledge: refers to knowledge about oneself as a learner and about what factors can influence one's performance. Declarative knowledge can also be referred to as "world knowledge".
Procedural knowledge: refers to knowledge about doing things. This type of knowledge is displayed as heuristics and strategies. A high degree of procedural knowledge can allow individuals to perform tasks more automatically. This is achieved through a large variety of strategies that can be accessed more efficiently.
Conditional knowledge: refers to knowing when and why to use declarative and procedural knowledge. It allows students to allocate their resources when using strategies. This in turn allows the strategies to become more effective.
These types of metacognitive knowledge also include:

Content knowledge (declarative knowledge), which involves understanding of one's own capabilities, such as a student evaluating their own knowledge of a subject in a class. It is notable that not all metacognition is accurate. Studies have shown that students often mistake lack of effort with understanding in evaluating themselves and their overall knowledge of a concept. Also, greater confidence in having performed well is associated with less accurate metacognitive judgment of the performance.
Task knowledge (procedural knowledge), which is how one perceives the difficulty of a task which is the content, length, and the type of assignment. The study mentioned in Content knowledge also deals with a person's ability to evaluate the difficulty of a task related to their overall performance on the task. Again, the accuracy of this knowledge was skewed as students who thought their way was better/easier also seemed to perform worse on evaluations, while students who were rigorously and continually evaluated reported to not be as confident but still did better on initial evaluations.
Strategic knowledge (conditional knowledge) is one's own capability for using strategies to learn information. Young children are not particularly good at this; it is not until students are in upper elementary school that they begin to develop an understanding of effective strategies.
In short, strategic knowledge involves knowing what (factual or declarative knowledge), knowing when and why (conditional or contextual knowledge) and knowing how (procedural or methodological knowledge). 
Similar to metacognitive knowledge, metacognitive regulation or "regulation of cognition" contains three skills that are essential.""",
    tier=8,
    domain="methodology",
    source="Wikipedia, 'Metacognition'",
    source_url="https://en.wikipedia.org/wiki/Metacognition",
))

register_atom(Atom(
    atom_type="principle",
    name="minimal_axioms",
    content="""In mathematical logic, independence is the unprovability of some specific sentence from some specific set of other sentences. The sentences in this set are referred to as "axioms".
A sentence σ is independent of a given first-order theory T if T neither proves nor refutes σ; that is, it is impossible to prove σ from T, and it is also impossible to prove from T that σ is false. Sometimes, σ is said (synonymously) to be undecidable from T. (This concept is unrelated to the idea of "decidability" as in a decision problem.)
A theory T is independent if no axiom in T is provable from the remaining axioms in T. A theory for which there is an independent set of axioms is independently axiomatizable.


== Usage note ==
Some authors say that σ is independent of T when T simply cannot prove σ, and do not necessarily assert by this that T cannot refute σ. These authors will sometimes say "σ is independent of and consistent with T" to indicate that T can neither prove nor refute σ.


== Independence results in set theory ==
Many interesting statements in set theory are independent of Zermelo–Fraenkel set theory (ZF). The following statements in set theory are known to be independent of ZF, under the assumption that ZF is consistent:

The axiom of choice
The continuum hypothesis and the generalized continuum hypothesis
The Suslin conjecture
The following statements (none of which have been proved false) cannot be proved in ZFC (the Zermelo–Fraenkel set theory plus the axiom of choice) to be independent of ZFC, under the added hypothesis that ZFC is consistent. 

The existence of strongly inaccessible cardinals
The existence of large cardinals
The non-existence of Kurepa trees
The following statements are inconsistent with the axiom of choice, and therefore with ZFC. However they are probably independent of ZF, in a corresponding sense to the above: They cannot be proved in ZF, and few working set theorists expect to find a refutation in ZF. However ZF cannot prove that they are independent of ZF, even with the added hypothesis that ZF is consistent.

The axiom of determinacy
The axiom of real determinacy
AD+


== Complete (strong) independence ==
A set of sentences is independent, or simply independent, if no sentence in the set is provable from the others. This is equivalent to saying that for each sentence in the set there exists an interpretation under which that sentence is false but all the others are true. 
There is another sense of independence, called complete independence, or strong independence. A set of sentences is completely independent if for every subset, there exists an interpretation under which all the members of that subset are true and all the others are false. This is equivalent to saying that all combinations of the sentences being true or false are consistent.


== Applications to physical theory ==
Since 2000, logical independence has become understood as having crucial significance in the foundations of physics.


== See also ==
List of statements independent of ZFC
Parallel postulate for an example in geometry


== Notes ==


== References ==
Mendelson, Elliott (1997), An Introduction to Mathematical Logic (4th ed.), London: Chapman & Hall, ISBN 978-0-412-80830-2
Monk, J. Donald (1976), Mathematical Logic, Graduate Texts in Mathematics, Berlin, New York: Springer-Verlag, ISBN 978-0-387-90170-1
Stabler, Edward Russell (1948), An introduction to mathematical thought, Reading, Massachusetts: Addison-Wesley""",
    tier=8,
    domain="logic",
    source="Wikipedia, 'Independence (mathematical logic)'",
    source_url="https://en.wikipedia.org/wiki/Independence_%28mathematical_logic%29",
))

register_atom(Atom(
    atom_type="methodology",
    name="novel_problem",
    content="""Problem solving is the process of achieving a goal by overcoming obstacles, a frequent part of most activities. Problems in need of solutions range from simple personal tasks (e.g. how to turn on an appliance) to complex issues in business and technical fields. The former is an example of simple problem solving (SPS) addressing one issue, whereas the latter is complex problem solving (CPS) with multiple interrelated obstacles. Another classification of problem-solving tasks is into well-defined problems with specific obstacles and goals, and ill-defined problems in which the current situation is troublesome but it is not clear what kind of resolution to aim for. Similarly, one may distinguish formal or fact-based problems requiring psychometric intelligence, versus socio-emotional problems which depend on the changeable emotions of individuals or groups, such as tactful behavior, fashion, or gift choices.
Solutions require sufficient resources and knowledge to attain the goal. Professionals such as lawyers, doctors, programmers, and consultants are largely problem solvers for issues that require technical skills and knowledge beyond general competence. Many businesses have found profitable markets by recognizing a problem and creating a solution: the more widespread and inconvenient the problem, the greater the opportunity to develop a scalable solution.
There are many specialized problem-solving techniques and methods in fields such as science, engineering, business, medicine, mathematics, computer science, philosophy, and social organization. The mental techniques to identify, analyze, and solve problems are studied in psychology and cognitive sciences. Also widely researched are the mental obstacles that prevent people from finding solutions; problem-solving impediments include confirmation bias, mental set, and functional fixedness.


== Definition ==
The term problem solving has a slightly different meaning depending on the discipline. For instance, it is a mental process in psychology and a computerized process in computer science. There are two different types of problems: ill-defined and well-defined; different approaches are used for each. Well-defined problems have specific end goals and clearly expected solutions, while ill-defined problems do not. Well-defined problems allow for more initial planning than ill-defined problems. Solving problems sometimes involves dealing with pragmatics (the way that context contributes to meaning) and semantics (the interpretation of the problem). The ability to understand what the end goal of the problem is, and what rules could be applied, represents the key to solving the problem. Sometimes a problem requires abstract thinking or coming up with a creative solution.
Problem solving has two major domains: mathematical problem solving and personal problem solving. Each concerns some difficulty or barrier that is encountered.


=== Psychology ===
Problem solving in psychology refers to the process of finding solutions to problems encountered in life. Solutions to these problems are usually situation- or context-specific. The process starts with problem finding and problem shaping, in which the problem is discovered and simplified. The next step is to generate possible solutions and evaluate them. Finally a solution is selected to be implemented and verified. Problems have an end goal to be reached; how you get there depends upon problem orientation (problem-solving coping style and skills) and systematic analysis.
Mental health professionals study the human problem-solving processes using methods such as introspection, behaviorism, simulation, computer modeling, and experiment. Social psychologists look into the person-environment relationship aspect of the problem and independent and interdependent problem-solving methods. Problem solving has been defined as a higher-order cognitive process and intellectual function that requires the modulation and control of more routine or fundamental skills.
Empirical research shows many different strategies and factors influence everyday problem solving. Rehabilitation psychologists studying people with frontal lobe injuries have found that deficits in emotional control and reasoning can be re-mediated with effective rehabilitation and could improve the capacity of injured persons to resolve everyday problems. Interpersonal everyday problem solving is dependent upon personal motivational and contextual components. One such component is the emotional valence of "real-world" problems, which can either impede or aid problem-solving performance. Researchers have focused on the role of emotions in problem solving, demonstrating that poor emotional control can disrupt focus on the target task, impede problem resolution, and lead to negative outcomes such as fatigue, depression, and inertia. In conceptualization,human problem solving consists of two related processes: problem orientation, and the motivational/attitudinal/affective approach to problematic situations and problem-solving skills. People's strategies cohere with their goals and stem from the process of comparing oneself with others.


=== Cognitive sciences ===
Among the first experimental psychologists to study problem solving were the Gestaltists in Germany, such as Karl Duncker in The Psychology of Productive Thinking (1935). Perhaps best known is the work of Allen Newell and Herbert A. Simon.
Experiments in the 1960s and early 1970s asked participants to solve relatively simple, well-defined, but not previously seen laboratory tasks. These simple problems, such as the Tower of Hanoi, admitted optimal solutions that could be found quickly, allowing researchers to observe the full problem-solving process. Researchers assumed that these model problems would elicit the characteristic cognitive processes by which more complex "real world" problems are solved.
An outstanding problem-solving technique found by this research is the principle of decomposition.


=== Computer science ===

Much of computer science and artificial intelligence involves designing automated systems to solve a specified type of problem: to accept input data and calculate a correct or adequate response, reasonably quickly. Algorithms are recipes or instructions that direct such systems, written into computer programs.
Steps for designing such systems include problem determination, heuristics, root cause analysis, de-duplication, analysis, diagnosis, and repair. Analytic techniques include linear and nonlinear programming, queuing systems, and simulation. A large, perennial obstacle is to find and fix errors in computer programs: debugging.


=== Logic ===
Formal logic concerns issues like validity, truth, inference, argumentation, and proof. In a problem-solving context, it can be used to formally represent a problem as a theorem to be proved, and to represent the knowledge needed to solve the problem as the premises to be used in a proof that the problem has a solution.
The use of computers to prove mathematical theorems using formal logic emerged as the field of automated theorem proving in the 1950s. It included the use of heuristic methods designed to simulate human problem solving, as in the Logic Theory Machine, developed by Allen Newell, Herbert A. Simon and J. C. Shaw, as well as algorithmic methods such as the resolution principle developed by John Alan Robinson.
In addition to its use for finding proofs of mathematical theorems, automated theorem-proving has also been used for program verification in computer science. In 1958, John McCarthy proposed the advice taker, to represent information in formal logic and to derive answers to questions using automated theorem-proving.""",
    tier=8,
    domain="methodology",
    source="Wikipedia, 'Problem solving'",
    source_url="https://en.wikipedia.org/wiki/Problem_solving",
))

register_atom(Atom(
    atom_type="principle",
    name="solution_elegance",
    content="""Mathematical beauty is a type of aesthetic value that is experienced in doing or contemplating mathematics. The testimonies of mathematicians indicate that various aspects of mathematics—including results, formulae, proofs and theories—can trigger subjective responses similar to the beauty of art, music, or nature. The pleasure in this experience can serve as a motivation for doing mathematics, and some mathematicians, such as G.H. Hardy, have characterized mathematics as an art form that seeks beauty.  
Beauty in mathematics has been subject to examination by mathematicians themselves and by philosophers, psychologists, and neuroscientists. Understanding beauty in general can be difficult because it is a subjective response to sense-experience but is perceived as a property of an external object, and because it may be shaped by cultural influence or personal experience. Mathematical beauty presents additional problems, since the aesthetic response is evoked by abstract ideas which can be communicated symbolically, and which may only be available to a minority of people with mathematical ability and training. The appreciation of mathematics may also be less passive than (for example) listening to music.
Furthermore, beauty in mathematics may be connected to other aesthetic or non-aesthetic values. Some authors identify mathematical elegance with mathematical beauty; others distinguish elegance as a separate aesthetic value, or as being, for instance, limited to the form of mathematical exposition. Beauty itself is often linked to, or thought to be dependent on, the abstractness, purity, simplicity, depth or order of mathematics.


== Examples of beautiful mathematics ==


=== Results ===

Euler's identity is often given as an example of a beautiful result:

  
    
      
        
          
            
              e
            
            
              
                i
              
              π
            
          
          +
          1
          =
          0
          
          .
        
      
    
    {\\displaystyle \\displaystyle \\mathrm {e} ^{\\mathrm {i} \\pi }+1=0\\,.}
  

This expression ties together arguably the five most important mathematical constants (e, i, π, 1, and 0) with the two most common mathematical symbols (+, =). Euler's identity is a special case of Euler's formula, which the physicist Richard Feynman called "our jewel" and "the most remarkable formula in mathematics".
Another example is Fermat's theorem on sums of two squares, which says that any prime number such that 
  
    
      
        p
        ≡
        1
        
          
          (
          mod
          
          4
          )
        
      
    
    {\\displaystyle p\\equiv 1{\\pmod {4}}}
  
 can be written as a sum of two square numbers (for example, 
  
    
      
        5
        =
        
          1
          
            2
          
        
        +
        
          2
          
            2
          
        
      
    
    {\\displaystyle 5=1^{2}+2^{2}}
  
, 
  
    
      
        13
        =
        
          2
          
            2
          
        
        +
        
          3
          
            2
          
        
      
    
    {\\displaystyle 13=2^{2}+3^{2}}
  
, 
  
    
      
        37
        =
        
          1
          
            2
          
        
        +
        
          6
          
            2
          
        
      
    
    {\\displaystyle 37=1^{2}+6^{2}}
  
), which both G.H. Hardy and E.T. Bell thought was a beautiful result.
In a survey in which mathematicians were asked to evaluate 24 theorems for their beauty, the top-rated three theorems were: Euler's equation; Euler's polyhedron formula, which asserts that for a polyhedron with V vertices, E edges, and F faces, 
  
    
      
        V
        −
        E
        +
        F
        =
        2
      
    
    {\\displaystyle V-E+F=2}
  
; and
Euclid's theorem that there are infinitely many prime numbers, which was also given by Hardy as an example of a beautiful theorem.


=== Proofs ===

Cantor's diagonal argument, which establishes that there are infinite sets which cannot be put into one-to-one correspondence with the infinite set of natural numbers, has been cited by both mathematicians and philosophers as an example of a beautiful proof.

Visual proofs, such as the illustrated proof of the Pythagorean theorem, and other proofs without words generally, such as the shown proof that the sum of all positive odd numbers up to 2n − 1 is a perfect square, have been thought beautiful.
The mathematician Paul Erdős spoke of The Book, an imaginary infinite book in which God has written down all the most beautiful mathematical proofs. When Erdős wanted to express particular appreciation of a proof, he would proclaim it "straight from The Book!". His rhetorical device inspired the creation of Proofs from THE BOOK, a collection of such proofs, including many suggested by Erdős himself.


=== Objects ===
In Plato's Timaeus, the five regular convex polyhedra, called the Platonic solids for their role in this dialogue, are called the "most beautiful" ("κάλλιστα") bodies. In the Timaeus, they are described as having been used by the demiurge, or creator-craftsman who builds the cosmos, for the four classical elements plus the heavens, because of their beauty.

In his 1596 book Mysterium Cosmographicum, Johannes Kepler argued that the orbits of the then-known planets in the Solar System have been arranged by God to correspond to a concentric arrangement of the five Platonic solids, each orbit lying on the circumsphere of one polyhedron and the insphere of another. For Kepler, God had wanted to shape the universe according to the five regular solids because of their beauty, and this explained why there were six planets (according to the knowledge of the time).

A more modern example is the exceptional simple Lie group 
  
    
      
        
          E
          
            8
          
        
      
    
    {\\displaystyle E_{8}}
  
, which has been called "perhaps the most beautiful structure in all of mathematics".


=== Scientific theories ===
The mathematical statements of scientific theories, especially in physics, are sometimes considered to be mathematically beautiful.""",
    tier=8,
    domain="methodology",
    source="Wikipedia, 'Mathematical beauty'",
    source_url="https://en.wikipedia.org/wiki/Mathematical_beauty",
))

register_atom(Atom(
    atom_type="theorem",
    name="algorithm_improvement",
    content="""In computer science, program optimization, code optimization, or software optimization is the process of modifying a software system to make some aspect of it work more efficiently or use fewer resources. In general, a computer program may be optimized so that it executes more rapidly, or to make it capable of operating with less memory storage or other resources, or draw less power.""",
    tier=9,
    domain="computer_science",
    source="Wikipedia, 'Program optimization'",
    source_url="https://en.wikipedia.org/wiki/Program_optimization",
))

register_atom(Atom(
    atom_type="theorem",
    name="impossibility_proof",
    content="""A comparison sort is a type of sorting algorithm that only reads the list elements through a single abstract comparison operation (often a "less than or equal to" operator or a three-way comparison) that determines which of two elements should occur first in the final sorted list. The only requirement is that the operator forms a total preorder over the data; that is:

if a ≤ b and b ≤ c then a ≤ c (transitivity)
for all a and b, a ≤ b or b ≤ a (connexity).
It is possible that both a ≤ b and b ≤ a with a ≠ b; in this case either may come first in the sorted list. In a stable sort, the input order determines the sorted order in this case.
Comparison sorts studied in the literature are "comparison-based". Elements a and b can be swapped or otherwise re-arranged by the algorithm only when the order between these elements has been established based on the outcomes of prior comparisons. This is the case when the order between a and b can be derived via the transitive closure of these prior comparison outcomes. 
For comparison-based sorts, the decision to execute basic operations other than comparisons is based on the outcome of comparisons. Hence in a time analysis, the number of executed comparisons is used to determine upper bound estimates for the number of executed basic operations such as swaps or assignments.    
A metaphor for thinking about comparison sorts is that someone has a set of unlabelled weights and a balance scale. Their goal is to line up the weights in order by their weight without any information except that obtained by placing two weights on the scale and seeing which one is heavier (or if they weigh the same).


== Examples ==

Some of the most well-known comparison sorts include:

Quicksort
Heapsort
Shellsort
Merge sort
Introsort
Insertion sort
Selection sort
Bubble sort
Odd–even sort
Cocktail shaker sort
Cycle sort
Merge-insertion sort
Smoothsort
Timsort
Block sort


== Performance limits and advantages of different sorting techniques ==
There are fundamental limits on the performance of comparison sorts. A comparison sort must have an average-case lower bound of Ω(n log n) comparison operations, which is known as linearithmic time. This is a consequence of the limited information available through comparisons alone — or, to put it differently, of the vague algebraic structure of totally ordered sets. In this sense, mergesort, heapsort, and introsort are asymptotically optimal in terms of the number of comparisons they must perform, although this metric neglects other operations. Non-comparison sorts (such as the examples discussed below) can achieve O(n) performance by using operations other than comparisons, allowing them to sidestep this lower bound (assuming elements are constant-sized).
Comparison sorts may run faster on some lists; many adaptive sorts such as insertion sort run in O(n) time on an already-sorted or nearly-sorted list. The Ω(n log n) lower bound applies only to the case in which the input list can be in any possible order.
Real-world measures of sorting speed may need to take into account the ability of some algorithms to optimally use relatively fast cached computer memory, or the application may benefit from sorting methods where sorted data begins to appear to the user quickly (and then user's speed of reading will be the limiting factor) as opposed to sorting methods where no output is available until the whole list is sorted.
Despite these limitations, comparison sorts offer the notable practical advantage that control over the comparison function allows sorting of many different datatypes and fine control over how the list is sorted. For example, reversing the result of the comparison function allows the list to be sorted in reverse; and one can sort a list of tuples in lexicographic order by just creating a comparison function that compares each part in sequence:

function tupleCompare((lefta, leftb, leftc), (righta, rightb, rightc))
    if lefta ≠ righta
        return compare(lefta, righta)
    else if leftb ≠ rightb
        return compare(leftb, rightb)
    else
        return compare(leftc, rightc)

Comparison sorts generally adapt more easily to complex orders such as the order of floating-point numbers. Additionally, once a comparison function is written, any comparison sort can be used without modification; non-comparison sorts typically require specialized versions for each datatype.
This flexibility, together with the efficiency of the above comparison sorting algorithms on modern computers, has led to widespread preference for comparison sorts in most practical work.


== Alternatives ==
Some sorting problems admit a strictly faster solution than the Ω(n log n) bound for comparison sorting by using non-comparison sorts; an example is integer sorting, where all keys are integers. When the keys form a small (compared to n) range, counting sort is an example algorithm that runs in linear time. Other integer sorting algorithms, such as radix sort, are not asymptotically faster than comparison sorting, but can be faster in practice.
The problem of sorting pairs of numbers by their sum is not subject to the Ω(n² log n) bound either (the square resulting from the pairing up); the best known algorithm still takes O(n² log n) time, but only O(n²) comparisons.


== Number of comparisons required to sort a list ==

The number of comparisons that a comparison sort algorithm requires increases in proportion to 
  
    
      
        n
        log
        ⁡
        (
        n
        )
      
    
    {\\displaystyle n\\log(n)}
  
, where n is the number of elements to sort.  This bound is asymptotically tight.
Given a list of distinct numbers (we can assume this because this is a worst-case analysis), there are n factorial permutations exactly one of which is the list in sorted order. The sort algorithm must gain enough information from the comparisons to identify the correct permutation. If the algorithm always completes after at most 
  
    
      
        f
        (
        n
        )
      
    
    {\\displaystyle f(n)}
  
 steps, it cannot distinguish more than 
  
    
      
        
          2
          
            f
            (
            n
            )
          
        
      
    
    {\\displaystyle 2^{f(n)}}
  
 cases because the keys are distinct and each comparison has only two possible outcomes.""",
    tier=9,
    domain="computer_science",
    source="Wikipedia, 'Comparison sort'",
    source_url="https://en.wikipedia.org/wiki/Comparison_sort",
))

register_atom(Atom(
    atom_type="methodology",
    name="failure_analysis",
    content="""In engineering, debugging is the process of finding the root cause, workarounds, and possible fixes for bugs.
For software, debugging tactics can involve interactive debugging, control flow analysis, log file analysis, monitoring at the application or system level, memory dumps, and profiling. Many programming languages and software development tools also offer programs to aid in debugging, known as debuggers.


== Etymology ==

The term bug, in the sense of defect, dates back at least to 1878 when Thomas Edison wrote "little faults and difficulties" in his inventions as "Bugs".
A popular story from the 1940's is from Admiral Grace Hopper. While she was working on a Mark II computer at Harvard University, her associates discovered a moth stuck in a relay that impeded operation and wrote in a log book "First actual case of a bug being found". Although probably a joke, conflating the two meanings of bug (biological and defect), the story indicates that the term was used in the computer field at that time.
Similarly, the term debugging was used in aeronautics before entering the world of computers. A letter from J. Robert Oppenheimer, director of the WWII atomic bomb Manhattan Project at Los Alamos, used the term in a letter to Dr. Ernest Lawrence at UC Berkeley, dated October 27, 1944, regarding the recruitment of additional technical staff.
The Oxford English Dictionary entry for debug uses the term debugging in reference to airplane engine testing in a 1945 article in the Journal of the Royal Aeronautical Society. 
An article in "Airforce" (June 1945 p. 50) refers to debugging aircraft cameras. 
The seminal article by Gill in 1951 is the earliest in-depth discussion of programming errors, but it does not use the term bug or debugging.
In the ACM's digital library, the term debugging is first used in three papers from the 1952 ACM National Meetings. Two of the three use the term in quotation marks.
By 1963, debugging was a common enough term to be mentioned in passing without explanation on page 1 of the CTSS manual.


== Scope ==
As software and electronic systems have become generally more complex, the various common debugging techniques have expanded with more methods to detect anomalies, assess impact, and schedule software patches or full updates to a system. The words "anomaly" and "discrepancy" can be used, as being more neutral terms, to avoid the words "error" and "defect" or "bug" where there might be an implication that all so-called errors, defects or bugs must be fixed (at all costs). Instead, an impact assessment can be made to determine if changes to remove an anomaly (or discrepancy) would be cost-effective for the system, or perhaps a scheduled new release might render the change(s) unnecessary. Not all issues are safety-critical or mission-critical in a system. Also, it is important to avoid the situation where a change might be more upsetting to users, long-term, than living with the known problem(s) (where the "cure would be worse than the disease"). Basing decisions of the acceptability of some anomalies can avoid a culture of a "zero-defects" mandate, where people might be tempted to deny the existence of problems so that the result would appear as zero defects. Considering the collateral issues, such as the cost-versus-benefit impact assessment, then broader debugging techniques will expand to determine the frequency of anomalies (how often the same "bugs" occur) to help assess their impact to the overall system.


== Tools ==

Debugging ranges in complexity from fixing simple errors to performing lengthy and tiresome tasks of data collection, analysis, and scheduling updates. The debugging skill of the programmer can be a major factor in the ability to debug a problem, but the difficulty of software debugging varies greatly with the complexity of the system, and also depends, to some extent, on the programming language(s) used and the available tools, such as debuggers. Debuggers are software tools which enable the programmer to monitor the execution of a program, stop it, restart it, set breakpoints, and change values in memory. The term debugger can also refer to the person who is doing the debugging.
Generally, high-level programming languages, such as Java, make debugging easier, because they have features such as exception handling and type checking that make real sources of erratic behaviour easier to spot. In programming languages such as C or assembly, bugs may cause silent problems such as memory corruption, and it is often difficult to see where the initial problem happened. In those cases, memory debugger tools may be needed.
In certain situations, general purpose software tools that are language specific in nature can be very useful. These take the form of static code analysis tools. These tools look for a very specific set of known problems, some common and some rare, within the source code, concentrating more on the semantics (e.g. data flow) rather than the syntax, as compilers and interpreters do.
Both commercial and free tools exist for various languages; some claim to be able to detect hundreds of different problems. These tools can be extremely useful when checking very large source trees, where it is impractical to do code walk-throughs. A typical example of a problem detected would be a variable dereference that occurs before the variable is assigned a value. As another example, some such tools perform strong type checking when the language does not require it. Thus, they are better at locating likely errors in code that is syntactically correct. But these tools have a reputation of false positives, where correct code is flagged as dubious. The old Unix lint program is an early example.
For debugging electronic hardware (e.g., computer hardware) as well as low-level software (e.g., BIOSes, device drivers) and firmware, instruments such as oscilloscopes, logic analyzers, or in-circuit emulators (ICEs) are often used, alone or in combination. An ICE may perform many of the typical software debugger's tasks on low-level software and firmware.


== Debugging process ==
The debugging process normally begins with identifying the steps to reproduce the problem. This can be a non-trivial task, particularly with parallel processes and some Heisenbugs for example. The specific user environment and usage history can also make it difficult to reproduce the problem.
After the bug is reproduced, the input of the program may need to be simplified to make it easier to debug. For example, a bug in a compiler can make it crash when parsing a large source file. However, after simplification of the test case, only few lines from the original source file can be sufficient to reproduce the same crash. Simplification may be done manually using a divide-and-conquer approach, in which the programmer attempts to remove some parts of original test case then checks if the problem still occurs. When debugging in a GUI, the programmer can try skipping some user interaction from the original problem description to check if the remaining actions are sufficient for causing the bug to occur.
After the test case is sufficiently simplified, a programmer can use a debugger tool to examine program states (values of variables, plus the call stack) and track down the origin of the problem(s). Alternatively, tracing can be used. In simple cases, tracing is just a few print statements which output the values of variables at particular points during the execution of the program.


== Techniques ==
Interactive debugging uses debugger tools which allow a program's execution to be processed one step at a time and to be paused to inspect or alter its state. Subroutines or function calls may typically be executed at full speed and paused again upon return to their caller, or themselves single stepped, or any mixture of these options.""",
    tier=9,
    domain="computer_science",
    source="Wikipedia, 'Debugging'",
    source_url="https://en.wikipedia.org/wiki/Debugging",
))

register_atom(Atom(
    atom_type="principle",
    name="invariant_discovery",
    content="""In mathematics, an invariant is a property of a mathematical object (or a class of mathematical objects) which remains unchanged after operations or transformations of a certain type are applied to the objects. The particular class of objects and type of transformations are usually indicated by the context in which the term is used. For example, the area of a triangle is an invariant with respect to isometries of the Euclidean plane. The phrases "invariant under" and "invariant to" a transformation are both used. More generally, an invariant with respect to an equivalence relation is a property that is constant on each equivalence class.
Invariants are used in diverse areas of mathematics such as geometry, topology, algebra and discrete mathematics. Some important classes of transformations are defined by an invariant they leave unchanged. For example, conformal maps are defined as transformations of the plane that preserve angles. The discovery of invariants is an important step in the process of classifying mathematical objects.


== Examples ==
A simple example of invariance is expressed in our ability to count. For a finite set of objects of any kind, there is a number to which we always arrive, regardless of the order in which we count the objects in the set. The quantity—a cardinal number—is associated with the set, and is invariant under the process of counting.
An identity is an equation that remains true for all values of its variables. There are also inequalities that remain true when the values of their variables change.
The distance between two points on a number line is not changed by adding the same quantity to both numbers. On the other hand, multiplication does not have this same property, as distance is not invariant under multiplication.
Angles and ratios of distances are invariant under scalings, rotations, translations and reflections. These transformations produce similar shapes, which are the basis of trigonometry. In contrast, angles and ratios are not invariant under non-uniform scaling (such as stretching). The sum of a triangle's interior angles (180°) is invariant under all the above operations.  As another example, all circles are similar: they can be transformed into each other, and the ratio of the circumference to the diameter is invariant (denoted by the Greek letter π (pi)).
Some more complicated examples:

The real part and the absolute value of a complex number are invariant under complex conjugation.
The tricolorability of knots.
The degree of a polynomial is invariant under a linear change of variables.
The dimension and homology groups of a topological object are invariant under homeomorphism.
The number of fixed points of a dynamical system is invariant under many mathematical operations.
Euclidean distance is invariant under orthogonal transformations.
Area is invariant under linear maps which have determinant ±1 (see Equiareal map § Linear transformations).
Some invariants of projective transformations include collinearity of three or more points, concurrency of three or more lines, conic sections, and the cross-ratio.
The determinant, trace, eigenvectors, and eigenvalues of a linear endomorphism are invariant under a change of basis. In other words, the spectrum of a matrix is invariant under a change of basis.
The principal invariants of tensors do not change with rotation of the coordinate system (see Invariants of tensors).
The singular values of a matrix are invariant under orthogonal transformations.
Lebesgue measure is invariant under translations.
The variance of a probability distribution is invariant under translations of the real line. Hence the variance of a random variable is unchanged after the addition of a constant.
The fixed points of a transformation are the elements in the domain that are invariant under the transformation. They may, depending on the application, be called symmetric with respect to that transformation. For example, objects with translational symmetry are invariant under certain translations.
The integral 
  
    
      
        
          ∫
          
            M
          
        
        K
        
        d
        μ
      
    
    {\\textstyle \\int _{M}K\\,d\\mu }
  
 of the Gaussian curvature 
  
    
      
        K
      
    
    {\\displaystyle K}
  
 of a two-dimensional Riemannian manifold 
  
    
      
        (
        M
        ,
        g
        )
      
    
    {\\displaystyle (M,g)}
  
 is invariant under changes of the Riemannian metric 
  
    
      
        g
      
    
    {\\displaystyle g}
  
.  This is the Gauss–Bonnet theorem.


=== MU puzzle ===
The MU puzzle is a good example of a logical problem where determining an invariant is of use for an impossibility proof. The puzzle asks one to start with the word MI and transform it into the word MU, using in each step one of the following transformation rules:

If a string ends with an I, a U may be appended (xI → xIU)
The string after the M may be completely duplicated (Mx → Mxx)
Any three consecutive I's (III) may be replaced with a single U (xIIIy → xUy)
Any two consecutive U's may be removed (xUUy → xy)
An example derivation (with superscripts indicating the applied rules) is

MI →2 MII →2 MIIII →3 MUI →2 MUIUI →1 MUIUIU →2 MUIUIUUIUIU →4 MUIUIIUIU → ...
In light of this, one might wonder whether it is possible to convert MI into MU, using only these four transformation rules. One could spend many hours applying these transformation rules to strings. However, it might be quicker to find a property that is invariant to all rules (that is, not changed by any of them), and that demonstrates that getting to MU is impossible. By looking at the puzzle from a logical standpoint, one might realize that the only way to get rid of any I's is to have three consecutive I's in the string. This makes the following invariant interesting to consider:

The number of I's in the string is not a multiple of 3.
This is an invariant to the problem, if for each of the transformation rules the following holds: if the invariant held before applying the rule, it will also hold after applying it. Looking at the net effect of applying the rules on the number of I's and U's, one can see this actually is the case for all rules:

The table above shows clearly that the invariant holds for each of the possible transformation rules, which means that whichever rule one picks, at whatever state, if the number of I's was not a multiple of three before applying the rule, then it  will not be afterwards either.
Given that there is a single I in the starting string MI, and one is not a multiple of three, one can then conclude that it is impossible to go from MI to MU (as the number of I's will never be a multiple of three).


== Invariant set ==
A subset S of the domain U of a mapping T: U → U  is an invariant set under the mapping when 
  
    
      
        x
        ∈
        S
        
        ⟺
        
        T
        (
        x
        )
        ∈
        S
        .
      
    
    {\\displaystyle x\\in S\\iff T(x)\\in S.}
  
 The elements of S are not necessarily fixed, even though the set S is fixed in the power set of U. (Some authors use the terminology setwise invariant, vs. pointwise invariant, to distinguish between these cases.)
For example, a circle is an invariant subset of the plane under a rotation about the circle's center. Further, a conical surface is invariant as a set under a homothety of space.
An invariant set of an operation T is also said to be stable under T.""",
    tier=9,
    domain="mathematics",
    source="Wikipedia, 'Invariant (mathematics)'",
    source_url="https://en.wikipedia.org/wiki/Invariant_%28mathematics%29",
))

register_atom(Atom(
    atom_type="principle",
    name="complexity_comparison",
    content="""In theoretical computer science and mathematics, computational complexity theory focuses on classifying computational problems according to their resource usage, and explores the relationships between these classifications. A computational problem is a task solved by a computer and is solvable by mechanical application of mathematical steps, such as an algorithm.
A problem is regarded as inherently difficult if its solution requires significant resources, whatever the algorithm used. The theory formalizes this intuition, by introducing mathematical models of computation to study these problems and quantifying their computational complexity, i.e., the amount of resources needed to solve them, such as time and storage. 
Other measures of complexity are also used, such as the amount of communication (used in communication complexity), the number of gates in a circuit (used in circuit complexity) and the number of processors (used in parallel computing). One of the roles of computational complexity theory is to determine the practical limits on what computers can and cannot do. The P versus NP problem, one of the seven Millennium Prize Problems, is part of the field of computational complexity.
Closely related fields in theoretical computer science are analysis of algorithms and computability theory. A key distinction between analysis of algorithms and computational complexity theory is that the former is devoted to analyzing the amount of resources needed by a particular algorithm to solve a problem, whereas the latter asks a more general question about all possible algorithms that could be used to solve the same problem. More precisely, computational complexity theory tries to classify problems that can or cannot be solved with appropriately restricted resources. In turn, imposing restrictions on the available resources is what distinguishes computational complexity from computability theory: the latter theory asks what kinds of problems can, in principle, be solved algorithmically.


== Computational problems ==


=== Problem instances ===
A computational problem can be viewed as an infinite collection of instances together with a set (possibly empty) of solutions for every instance. The input string for a computational problem is referred to as a problem instance, and should not be confused with the problem itself. In computational complexity theory, a problem refers to the abstract question to be solved. In contrast, an instance of this problem is a rather concrete utterance, which can serve as the input for a decision problem. For example, consider the problem of primality testing. The instance is a number (e.g., 15) and the solution is "yes" if the number is prime and "no" otherwise (in this case, 15 is not prime and the answer is "no"). Stated another way, the instance is a particular input to the problem, and the solution is the output corresponding to the given input.
To further highlight the difference between a problem and an instance, consider the following instance of the decision version of the travelling salesman problem: Is there a route of at most 2000 kilometres passing through all of Germany's 14 largest cities? The quantitative answer to this particular problem instance is of little use for solving other instances of the problem, such as asking for a round trip through 14 sites in Milan whose total length is at most 10 km. For this reason, complexity theory addresses computational problems and not particular problem instances.


=== Representing problem instances ===
When considering computational problems, a problem instance is a string over an alphabet. Usually, the alphabet is taken to be the binary alphabet (i.e., the set {0,1}), and thus the strings are bitstrings. As in a real-world computer, mathematical objects other than bitstrings must be suitably encoded. For example, integers can be represented in binary notation, and graphs can be encoded directly via their adjacency matrices, or by encoding their adjacency lists in binary.
Even though some proofs of complexity-theoretic theorems regularly assume some concrete choice of input encoding, one tries to keep the discussion abstract enough to be independent of the precise choice of encoding. This can be achieved by ensuring that different representations can be transformed into each other efficiently.


=== Decision problems as formal languages ===

Decision problems are one of the central objects of study in computational complexity theory. A decision problem is a type of computational problem where the answer is either yes or no (alternatively, 1 or 0). A decision problem can be viewed as a formal language, where the members of the language are instances whose output is yes, and the non-members are those instances whose output is no. The objective is to decide, with the aid of an algorithm, whether a given input string is a member of the formal language under consideration. If the algorithm deciding this problem returns the answer yes, the algorithm is said to accept the input string, otherwise it is said to reject the input.
An example of a decision problem is the following. The input is an arbitrary graph. The problem consists in deciding whether the given graph is connected or not. The formal language associated with this decision problem is then the set of all connected graphs—to obtain a precise definition of this language, one has to decide how graphs are encoded as binary strings.


=== Function problems ===
A function problem is a computational problem where a single output (of a total function) is expected for every input, but the output can be more complex than that of a decision problem—that is, the output is not just yes or no. Notable examples include the traveling salesman problem and the integer factorization problem.
It is tempting to think that the notion of function problems is much richer than the notion of decision problems. However, this is not really the case, since function problems can be recast as decision problems. For example, the multiplication of two integers can be expressed as the set of triples 
  
    
      
        (
        a
        ,
        b
        ,
        c
        )
      
    
    {\\displaystyle (a,b,c)}
  
 such that the relation 
  
    
      
        a
        ×
        b
        =
        c
      
    
    {\\displaystyle a\\times b=c}
  
 holds. Deciding whether a given triple is a member of this set corresponds to solving the problem of multiplying two numbers.


=== Measuring the size of an instance ===
To measure the difficulty of solving a computational problem, one may wish to see how much time the best algorithm requires to solve the problem. However, the running time may, in general, depend on the instance. In particular, larger instances will require more time to solve. Thus the time required to solve a problem (or the space required, or any measure of complexity) is calculated as a function of the size of the instance. The input size is typically measured in bits. Complexity theory studies how algorithms scale as input size increases. For instance, in the problem of finding whether a graph is connected, how much more time does it take to solve a problem for a graph with 
  
    
      
        2
        n
      
    
    {\\displaystyle 2n}
  
 vertices compared to the time taken for a graph with 
  
    
      
        n
      
    
    {\\displaystyle n}
  
 vertices?
If the input size is 
  
    
      
        n
      
    
    {\\displaystyle n}
  
, the time taken can be expressed as a function of 
  
    
      
        n
      
    
    {\\displaystyle n}
  
. Since the time taken on different inputs of the same size can be different, the worst-case time complexity 
  
    
      
        T
        (
        n
        )
      
    
    {\\displaystyle T(n)}
  
 is defined to be the maximum time taken over all inputs of size 
  
    
      
        n
      
    
    {\\displaystyle n}
  
.""",
    tier=9,
    domain="computer_science",
    source="Wikipedia, 'Computational complexity theory'",
    source_url="https://en.wikipedia.org/wiki/Computational_complexity_theory",
))

register_atom(Atom(
    atom_type="theorem",
    name="reduction",
    content="""In computability theory and computational complexity theory, a reduction is an algorithm for transforming one problem into another problem. A sufficiently efficient reduction from one problem to another may be used to show that the second problem is at least as difficult as the first.
Intuitively, problem A is reducible to problem B, if an algorithm for solving problem B efficiently (if it exists) could also be used as a subroutine to solve problem A efficiently. When this is true, solving A cannot be harder than solving B. "Harder" means having a higher estimate of the required computational resources in a given context (e.g., higher time complexity, greater memory requirement, need for extra hardware processor cores for a parallel solution compared to a single-threaded solution, etc.). The existence of a reduction from A to B can be written in the shorthand notation A ≤m B, usually with a subscript on the ≤ to indicate the type of reduction being used (m : many-one reduction, p : polynomial reduction).
The mathematical structure generated on a set of problems by the reductions of a particular type generally forms a preorder, whose equivalence classes may be used to define degrees of unsolvability and complexity classes.


== Introduction ==
There are two main situations where we need to use reductions:

First, we find ourselves trying to solve a problem that is similar to a problem we've already solved. In these cases, often a quick way of solving the new problem is to transform each instance of the new problem into instances of the old problem, solve these using our existing solution, and then use these to obtain our final solution. This is perhaps the most obvious use of reductions.
Second: suppose we have a problem that we've proven is hard to solve, and we have a similar new problem. We might suspect that it is also hard to solve. We argue by contradiction: suppose the new problem is easy to solve. Then, if we can show that every instance of the old problem can be solved easily by transforming it into instances of the new problem and solving those, we have a contradiction. This establishes that the new problem is also hard.
A very simple example of a reduction is from multiplication to squaring. Suppose all we know how to do is to add, subtract, take squares, and divide by two. We can use this knowledge, combined with the following formula, to obtain the product of any two numbers:

  
    
      
        a
        ×
        b
        =
        
          
            
              (
              
                
                  
                    (
                    
                      a
                      +
                      b
                    
                    )
                  
                  
                    2
                  
                
                −
                
                  a
                  
                    2
                  
                
                −
                
                  b
                  
                    2
                  
                
              
              )
            
            2
          
        
      
    
    {\\displaystyle a\\times b={\\frac {\\left(\\left(a+b\\right)^{2}-a^{2}-b^{2}\\right)}{2}}}
  

We also have a reduction in the other direction; obviously, if we can multiply two numbers, we can square a number. This seems to imply that these two problems are equally hard. This kind of reduction corresponds to Turing reduction.
However, the reduction becomes much harder if we add the restriction that we can only use the squaring function one time, and only at the end. In this case, even if we're allowed to use all the basic arithmetic operations, including multiplication, no reduction exists in general, because in order to get the desired result as a square we have to compute its square root first, and this square root could be an irrational number like 
  
    
      
        
          
            2
          
        
      
    
    {\\displaystyle {\\sqrt {2}}}
  
 that cannot be constructed by arithmetic operations on rational numbers. Going in the other direction, however, we can certainly square a number with just one multiplication, only at the end. Using this limited form of reduction, we have shown the unsurprising result that multiplication is harder in general than squaring. This corresponds to many-one reduction.


== Properties ==
Reducibility is a preordering, that is, a reflexive and transitive relation, on P(N)×P(N), where P(N) is the power set of the natural numbers.


== Types and applications of reductions ==
As described in the example above, there are two main types of reductions used in computational complexity theory, the many-one reduction and the Turing reduction. Many-one reductions map instances of one problem to instances of another; Turing reductions compute the solution to one problem, assuming the other problem is easy to solve. The many-one reduction is a stronger type of Turing reduction, and is more effective at separating problems into distinct complexity classes. However, the increased restrictions on many-one reductions make them more difficult to find.
A problem is complete for a complexity class if every problem in the class reduces to that problem, and it is also in the class itself. In this sense the problem represents the class, since any solution to it can, in combination with the reductions, be used to solve every problem in the class.
However, in order to be useful, reductions must be easy. For example, it's quite possible to reduce a difficult-to-solve NP-complete problem like the boolean satisfiability problem to a trivial problem, like determining if a number equals zero, by having the reduction machine solve the problem in exponential time and output zero only if there is a solution. However, this does not achieve much, because even though we can solve the new problem, performing the reduction is just as hard as solving the old problem. Likewise, a reduction computing a noncomputable function can reduce an undecidable problem to a decidable one. As Michael Sipser points out in Introduction to the Theory of Computation: "The reduction must be easy, relative to the complexity of typical problems in the class [...] If the reduction itself were difficult to compute, an easy solution to the complete problem wouldn't necessarily yield an easy solution to the problems reducing to it."
Therefore, the appropriate notion of reduction depends on the complexity class being studied. When studying the complexity class NP and many harder classes such as the polynomial hierarchy, polynomial-time reductions are used. When studying classes within P such as NC and NL, log-space reductions are used. Reductions are also used in computability theory to show whether problems are or are not solvable by machines at all; in this case, reductions are restricted only to computable functions (for many-one reductions) or oracle machines (for Turing reductions).
In the case of optimization (maximization or minimization) problems, we often think in terms of approximation-preserving reductions. Suppose we have two optimization problems such that instances of one problem can be mapped onto instances of the other, in a way that nearly optimal solutions to instances of the latter problem can be transformed back to yield nearly optimal solutions to the former. This way, if we have an optimization algorithm (or approximation algorithm) that finds near-optimal (or optimal) solutions to instances of problem B, and an efficient approximation-preserving reduction from problem A to problem B, by composition we obtain an optimization algorithm that yields near-optimal solutions to instances of problem A.""",
    tier=9,
    domain="computer_science",
    source="Wikipedia, 'Reduction (complexity)'",
    source_url="https://en.wikipedia.org/wiki/Reduction_%28complexity%29",
))

register_atom(Atom(
    atom_type="theorem",
    name="learning_bound",
    content="""In computational learning theory, probably approximately correct (PAC) learning is a framework for mathematical analysis of machine learning. It was proposed in 1984 by Leslie Valiant.
In this framework, the learner receives samples and must select a generalization function (called the hypothesis) from a certain class of possible functions. The goal is that, with high probability (the "probably" part), the selected function will have low generalization error (the "approximately correct" part). The learner must be able to learn the concept given any arbitrary approximation ratio, probability of success, or distribution of the samples.
The model was later extended to treat noise (misclassified samples). 
An important innovation of the PAC framework is the introduction of computational complexity theory concepts to machine learning. In particular, the learner is expected to find efficient functions (time and space requirements bounded to a polynomial of the example size), and the learner itself must implement an efficient procedure (requiring an example count bounded to a polynomial of the concept size, modified by the approximation and likelihood bounds).


== Definitions and terminology ==
In order to give the definition for something that is PAC-learnable, we first have to introduce some terminology.
For the following definitions, two examples will be used.  The first is the problem of character recognition given an array of 
  
    
      
        n
      
    
    {\\displaystyle n}
  
 bits encoding a binary-valued image.  The other example is the problem of finding an interval that will correctly classify points within the interval as positive and the points outside of the range as negative.
Let 
  
    
      
        X
      
    
    {\\displaystyle X}
  
 be a set called the instance space or the encoding of all the samples.  In the character recognition problem, the instance space is 
  
    
      
        X
        =
        {
        0
        ,
        1
        
          }
          
            n
          
        
      
    
    {\\displaystyle X=\\{0,1\\}^{n}}
  
.  In the interval problem the instance space, 
  
    
      
        X
      
    
    {\\displaystyle X}
  
, is the set of all bounded intervals in 
  
    
      
        
          R
        
      
    
    {\\displaystyle \\mathbb {R} }
  
, where 
  
    
      
        
          R
        
      
    
    {\\displaystyle \\mathbb {R} }
  
 denotes the set of all real numbers.
A concept is a subset 
  
    
      
        c
        ⊂
        X
      
    
    {\\displaystyle c\\subset X}
  
.  One concept is the set of all patterns of bits in 
  
    
      
        X
        =
        {
        0
        ,
        1
        
          }
          
            n
          
        
      
    
    {\\displaystyle X=\\{0,1\\}^{n}}
  
 that encode a picture of the letter "P".  An example concept from the second example is the set of open intervals, 
  
    
      
        {
        (
        a
        ,
        b
        )
        ∣
        0
        ≤
        a
        ≤
        π
        
          /
        
        2
        ,
        π
        ≤
        b
        ≤
        
          
            13
          
        
        }
      
    
    {\\displaystyle \\{(a,b)\\mid 0\\leq a\\leq \\pi /2,\\pi \\leq b\\leq {\\sqrt {13}}\\}}
  
, each of which contains only the positive points.  A concept class  
  
    
      
        C
      
    
    {\\displaystyle C}
  
 is a collection of concepts over 
  
    
      
        X
      
    
    {\\displaystyle X}
  
.  This could be the set of all subsets of the array of bits that are skeletonized 4-connected (width of the font is 1).
Let 
  
    
      
        EX
        ⁡
        (
        c
        ,
        D
        )
      
    
    {\\displaystyle \\operatorname {EX} (c,D)}
  
 be a procedure that draws an example, 
  
    
      
        x
      
    
    {\\displaystyle x}
  
, using a probability distribution 
  
    
      
        D
      
    
    {\\displaystyle D}
  
 and gives the correct label 
  
    
      
        c
        (
        x
        )
      
    
    {\\displaystyle c(x)}
  
, that is 1 if 
  
    
      
        x
        ∈
        c
      
    
    {\\displaystyle x\\in c}
  
 and 0 otherwise.
Now, given 
  
    
      
        0
        <
        ϵ
        ,
        δ
        <
        1
      
    
    {\\displaystyle 0<\\epsilon ,\\delta <1}
  
, assume there is an algorithm 
  
    
      
        A
      
    
    {\\displaystyle A}
  
 and a polynomial 
  
    
      
        p
      
    
    {\\displaystyle p}
  
 in 
  
    
      
        1
        
          /
        
        ϵ
        ,
        1
        
          /
        
        δ
      
    
    {\\displaystyle 1/\\epsilon ,1/\\delta }
  
 (and other relevant parameters of the class 
  
    
      
        C
      
    
    {\\displaystyle C}
  
) such that, given a sample of size 
  
    
      
        p
      
    
    {\\displaystyle p}
  
 drawn according to 
  
    
      
        EX
        ⁡
        (
        c
        ,
        D
        )
      
    
    {\\displaystyle \\operatorname {EX} (c,D)}
  
, then, with probability of at least 
  
    
      
        1
        −
        δ
      
    
    {\\displaystyle 1-\\delta }
  
, 
  
    
      
        A
      
    
    {\\displaystyle A}
  
 outputs a hypothesis 
  
    
      
        h
        ∈
        C
      
    
    {\\displaystyle h\\in C}
  
 that has an average error less than or equal to 
  
    
      
        ϵ
      
    
    {\\displaystyle \\epsilon }
  
 on 
  
    
      
        X
      
    
    {\\displaystyle X}
  
 with the same distribution 
  
    
      
        D
      
    
    {\\displaystyle D}
  
.  Further if the above statement for algorithm 
  
    
      
        A
      
    
    {\\displaystyle A}
  
 is true for every concept 
  
    
      
        c
        ∈
        C
      
    
    {\\displaystyle c\\in C}
  
 and for every distribution 
  
    
      
        D
      
    
    {\\displaystyle D}
  
 over 
  
    
      
        X
      
    
    {\\displaystyle X}
  
, and for all 
  
    
      
        0
        <
        ϵ
        ,
        δ
        <
        1
      
    
    {\\displaystyle 0<\\epsilon ,\\delta <1}
  
  then 
  
    
      
        C
      
    
    {\\displaystyle C}
  
 is (efficiently) PAC learnable (or distribution-free PAC learnable).  We can also say that 
  
    
      
        A
      
    
    {\\displaystyle A}
  
 is a PAC learning algorithm for 
  
    
      
        C
      
    
    {\\displaystyle C}
  
.


== Equivalence ==
Under some regularity conditions these conditions are equivalent: 

The concept class C is PAC learnable.
The VC dimension of C is finite.
C is a uniformly Glivenko-Cantelli class.
C is compressible in the sense of Littlestone and Warmuth


== See also ==
Data mining
Error tolerance (PAC learning)
Occam learning
Sample complexity


== References ==


== Further reading ==
M. Kearns, U. Vazirani. An Introduction to Computational Learning Theory. MIT Press, 1994. A textbook.
M. Mohri, A. Rostamizadeh, and A. Talwalkar. Foundations of Machine Learning. MIT Press, 2018. Chapter 2 contains a detailed treatment of PAC-learnability. Readable through open access from the publisher.
D. Haussler. Overview of the Probably Approximately Correct (PAC) Learning Framework. An introduction to the topic.
L. Valiant. Probably Approximately Correct. Basic Books, 2013. In which Valiant argues that PAC learning describes how organisms evolve and learn.
Littlestone, N.; Warmuth, M. K. (June 10, 1986). "Relating Data Compression and Learnability" (PDF). Archived from the original (PDF) on 2017-08-09.
Moran, Shay; Yehudayoff, Amir (2015). "Sample compression schemes for VC classes". arXiv:1503.06960 [cs.LG].


== External links ==
Interactive explanation of PAC learning""",
    tier=9,
    domain="machine_learning",
    source="Wikipedia, 'Probably approximately correct learning'",
    source_url="https://en.wikipedia.org/wiki/Probably_approximately_correct_learning",
))

register_atom(Atom(
    atom_type="methodology",
    name="hypothesis_design",
    content="""An experiment is a procedure carried out to support or refute a hypothesis, or determine the efficacy or likelihood of something previously untried.  Experiments provide insight into cause-and-effect by demonstrating what outcome occurs when a particular factor is manipulated.  Experiments vary greatly in goal and scale but always rely on repeatable procedure and logical analysis of the results. There also exist  natural experimental studies.
A child may carry out basic experiments to understand how things fall to the ground, while teams of scientists may take years of systematic investigation to advance their understanding of a phenomenon. Experiments and other types of hands-on activities are very important to student learning in the science classroom. Experiments can raise test scores and help a student become more engaged and interested in the material they are learning, especially when used over time. Experiments can vary from personal and informal natural comparisons (e.g. tasting a range of chocolates to find a favorite), to highly controlled (e.g. tests requiring complex apparatus overseen by many scientists that hope to discover information about subatomic particles). Uses of experiments vary considerably between the natural and human sciences.
Experiments typically include controls, which are designed to minimize the effects of variables other than the single independent variable. This increases the reliability of the results, often through a comparison between control measurements and the other measurements. Scientific controls are a part of the scientific method. Ideally, all variables in an experiment are controlled (accounted for by the control measurements) and none are uncontrolled. In such an experiment, if all controls work as expected, it is possible to conclude that the experiment works as intended, and that results are due to the effect of the tested variables.


== Overview ==
In the scientific method, an experiment is an empirical procedure that arbitrates competing models or hypotheses. Researchers also use experimentation to test existing theories or new hypotheses to support or disprove them.
An experiment usually tests a hypothesis, which is an expectation about how a particular process or phenomenon works. However, an experiment may also aim to answer a "what-if" question, without a specific expectation about what the experiment reveals, or to confirm prior results. If an experiment is carefully conducted, the results usually either support or disprove the hypothesis. According to some philosophies of science, an experiment can never "prove" a hypothesis, it can only add support. On the other hand, an experiment that provides a counterexample can disprove a theory or hypothesis, but a theory can always be salvaged by appropriate ad hoc modifications at the expense of simplicity.
An experiment must also control the possible confounding factors—any factors that would mar the accuracy or repeatability of the experiment or the ability to interpret the results. Confounding is commonly eliminated through scientific controls and/or, in randomized experiments, through random assignment.
In engineering and the physical sciences, experiments are a primary component of the scientific method. They are used to test theories and hypotheses about how physical processes work under particular conditions (e.g., whether a particular engineering process can produce a desired chemical compound). Typically, experiments in these fields focus on replication of identical procedures in hopes of producing identical results in each replication. Random assignment is uncommon.
In medicine and the social sciences, the prevalence of experimental research varies widely across disciplines. When used, however, experiments typically follow the form of the clinical trial, where experimental units (usually individual human beings) are randomly assigned to a treatment or control condition where one or more outcomes are assessed. In contrast to norms in the physical sciences, the focus is typically on the average treatment effect (the difference in outcomes between the treatment and control groups) or another test statistic produced by the experiment. A single study typically does not involve replications of the experiment, but separate studies may be aggregated through systematic review and meta-analysis.
There are various differences in experimental practice in each of the branches of science. For example, agricultural research frequently uses randomized experiments (e.g., to test the comparative effectiveness of different fertilizers), while experimental economics often involves experimental tests of theorized human behaviors without relying on random assignment of individuals to treatment and control conditions.


== History ==

Several scholars have noted that the account in Daniel 1:12–16 contains one of the earliest descriptions of a controlled comparative test in ancient literature. In the narrative, Daniel and his companions request a ten-day trial in which they consume only vegetables and water, while other youths continue on the king’s diet. The results of the two regimens are compared, and the steward is instructed to act based on the observable outcome.
Historians of science have occasionally referenced this passage as an early literary example of empirical reasoning. David C. Lindberg notes that the Hebrew Bible contains "procedures that resemble empirical testing," and includes Daniel 1 among examples where a trial is deliberately arranged to evaluate competing conditions. James C. VanderKam likewise describes the episode as presenting "a rudimentary experimental design" contrasting two diets under controlled circumstances. While this view is not universal, some commentators have referred to the episode as one of the earliest recorded experimental tests.
One of the first methodical approaches to experiments in the modern sense is visible in the works of the Arab mathematician and scholar Ibn al-Haytham. He conducted his experiments in the field of optics—going back to optical and mathematical problems in the works of Ptolemy—by controlling his experiments due to factors such as self-criticality, reliance on visible results of the experiments as well as a criticality in terms of earlier results. He was one of the first scholars to use an inductive-experimental method for achieving results. In his Book of Optics he describes the fundamentally new approach to knowledge and research in an experimental sense:

We should, that is, recommence the inquiry into its principles and premisses, beginning our investigation with an inspection of the things that exist and a survey of the conditions of visible objects. We should distinguish the properties of particulars, and gather by induction what pertains to the eye when vision takes place and what is found in the manner of sensation to be uniform, unchanging, manifest and not subject to doubt. After which we should ascend in our inquiry and reasonings, gradually and orderly, criticizing premisses and exercising caution in regard to conclusions—our aim in all that we make subject to inspection and review being to employ justice, not to follow prejudice, and to take care in all that we judge and criticize that we seek the truth and not to be swayed by opinion. We may in this way eventually come to the truth that gratifies the heart and gradually and carefully reach the end at which certainty appears; while through criticism and caution we may seize the truth that dispels disagreement and resolves doubtful matters. For all that, we are not free from that human turbidity which is in the nature of man; but we must do our best with what we possess of human power. From God we derive support in all things.
According to his explanation, a strictly controlled test execution with a sensibility for the subjectivity and susceptibility of outcomes due to the nature of man is necessary.""",
    tier=9,
    domain="methodology",
    source="Wikipedia, 'Experiment'",
    source_url="https://en.wikipedia.org/wiki/Experiment",
))

register_atom(Atom(
    atom_type="methodology",
    name="meta_pattern",
    content="""Pattern recognition is the task of assigning a class to an observation based on patterns extracted from data. While similar, pattern recognition (PR) is not to be confused with pattern machines (PM) which may possess PR capabilities but their primary function is to distinguish and create emergent  patterns.   PR has applications in statistical data analysis, signal processing, image analysis, information retrieval, bioinformatics, data compression, computer graphics and machine learning. Pattern recognition has its origins in statistics and engineering; some modern approaches to pattern recognition include the use of machine learning, due to the increased availability of big data and a new abundance of processing power.
Pattern recognition systems are commonly trained from labeled "training" data. When no labeled data are available, other algorithms can be used to discover previously unknown patterns. KDD and data mining have a larger focus on unsupervised methods and stronger connection to business use. Pattern recognition focuses more on the signal and also takes acquisition and signal processing into consideration. It originated in engineering, and the term is popular in the context of computer vision: a leading computer vision conference is named Conference on Computer Vision and Pattern Recognition.
In machine learning, pattern recognition is the assignment of a label to a given input value. In statistics, discriminant analysis was introduced for this same purpose in 1936. An example of pattern recognition is classification, which attempts to assign each input value to one of a given set of classes (for example, determine whether a given email is "spam"). Pattern recognition is a more general problem that encompasses other types of output as well. Other examples are regression, which assigns a real-valued output to each input; sequence labeling, which assigns a class to each member of a sequence of values (for example, part of speech tagging, which assigns a part of speech to each word in an input sentence); and parsing, which assigns a parse tree to an input sentence, describing the syntactic structure of the sentence.
Pattern recognition algorithms generally aim to provide a reasonable answer for all possible inputs and to perform "most likely" matching of the inputs, taking into account their statistical variation. This is opposed to pattern matching algorithms, which look for exact matches in the input with pre-existing patterns. A common example of a pattern-matching algorithm is regular expression matching, which looks for patterns of a given sort in textual data and is included in the search capabilities of many text editors and word processors.


== Overview ==

A modern definition of pattern recognition is:

The field of pattern recognition is concerned with the automatic discovery of regularities in data through the use of computer algorithms and with the use of these regularities to take actions such as classifying the data into different categories.
Pattern recognition is generally categorized according to the type of learning procedure used to generate the output value. Supervised learning assumes that a set of training data (the training set) has been provided, consisting of a set of instances that have been properly labeled by hand with the correct output. A learning procedure then generates a model that attempts to meet two sometimes conflicting objectives: Perform as well as possible on the training data, and generalize as well as possible to new data (usually, this means being as simple as possible, for some technical definition of "simple", in accordance with Occam's Razor, discussed below). Unsupervised learning, on the other hand, assumes training data that has not been hand-labeled, and attempts to find inherent patterns in the data that can then be used to determine the correct output value for new data instances. A combination of the two that has been explored is semi-supervised learning, which uses a combination of labeled and unlabeled data (typically a small set of labeled data combined with a large amount of unlabeled data). In cases of unsupervised learning, there may be no training data at all.
Sometimes different terms are used to describe the corresponding supervised and unsupervised learning procedures for the same type of output. The unsupervised equivalent of classification is normally known as clustering, based on the common perception of the task as involving no training data to speak of, and of grouping the input data into clusters based on some inherent similarity measure (e.g. the distance between instances, considered as vectors in a multi-dimensional vector space), rather than assigning each input instance into one of a set of pre-defined classes. In some fields, the terminology is different. In community ecology, the term classification is used to refer to what is commonly known as "clustering".
The piece of input data for which an output value is generated is formally termed an instance. The instance is formally described by a vector of features, which together constitute a description of all known characteristics of the instance. These feature vectors can be seen as defining points in an appropriate multidimensional space, and methods for manipulating vectors in vector spaces can be correspondingly applied to them, such as computing the dot product or the angle between two vectors. Features typically are either categorical (also known as nominal, i.e., consisting of one of a set of unordered items, such as a gender of "male" or "female", or a blood type of "A", "B", "AB" or "O"), ordinal (consisting of one of a set of ordered items, e.g., "large", "medium" or "small"), integer-valued (e.g., a count of the number of occurrences of a particular word in an email) or real-valued (e.g., a measurement of blood pressure). Often, categorical and ordinal data are grouped together, and this is also the case for integer-valued and real-valued data. Many algorithms work only in terms of categorical data and require that real-valued or integer-valued data be discretized into groups (e.g., less than 5, between 5 and 10, or greater than 10).


=== Probabilistic classifiers ===

Many common pattern recognition algorithms are probabilistic in nature, in that they use statistical inference to find the best label for a given instance. Unlike other algorithms, which simply output a "best" label, often probabilistic algorithms also output a probability of the instance being described by the given label. In addition, many probabilistic algorithms output a list of the N-best labels with associated probabilities, for some value of N, instead of simply a single best label. When the number of possible labels is fairly small (e.g., in the case of classification), N may be set so that the probability of all possible labels is output. Probabilistic algorithms have many advantages over non-probabilistic algorithms:

They output a confidence value associated with their choice. (Note that some other algorithms may also output confidence values, but in general, only for probabilistic algorithms is this value mathematically grounded in probability theory. Non-probabilistic confidence values can in general not be given any specific meaning, and only used to compare against other confidence values output by the same algorithm.)
Correspondingly, they can abstain when the confidence of choosing any particular output is too low.
Because of the probabilities output, probabilistic pattern-recognition algorithms can be more effectively incorporated into larger machine-learning tasks, in a way that partially or completely avoids the problem of error propagation.


=== Number of important feature variables ===
Feature selection algorithms attempt to directly prune out redundant or irrelevant features. A general introduction to feature selection which summarizes approaches and challenges, has been given.""",
    tier=9,
    domain="methodology",
    source="Wikipedia, 'Pattern recognition'",
    source_url="https://en.wikipedia.org/wiki/Pattern_recognition",
))

register_atom(Atom(
    atom_type="principle",
    name="representation_choice",
    content="""In computer science, a data structure is a way to organize and store data that is usually chosen for efficient access to data. More precisely, a data structure is the physical implementation of a data type, including specifications of the data organization and storage format, as well functions or operations for working with this data. Data structures are closely related to abstract data types (ADTs). The data structure describes the representation of data in memory and how operations are carried out, while the ADT describes the logical form or algebraic structure of the data type—what operations are allowed and what results they produce—without describing how those operations are implemented. Some authors do not use the term "abstract data type" and simply refer to the logical and physical forms of the data structure.


== Usage ==
Efficient data structures are essential for managing large datasets and are fundamental to algorithm design. Relational databases commonly use B-tree indice for data retrieval, while compiler implementations usually use hash tables to look up identifiers. Filesystems and search engines make extensive use of specialized data structures. Rob Pike has stated that the choice of data structure almost always has a greater impact on efficiency than the choice of algorithm, as the algorithm is often self-evident. Data structures are used to organize data in both primary memory (RAM) and secondary storage (such as disks).


== Implementation ==
Implementing a data structure involves writing a set of subroutines—such as insertion, deletion, traversal, or lookup—that create and manipulate instances of that structure. Data structures can be implemented using a variety of programming languages and techniques. A data structure corresponds directly to a single concrete implementation, in contrast to an ADT which describes behavior and operations independently of any particular implementation. There may be multiple concrete data structures for the same ADT, for example a linked list or a resizable array for the list ADT. As such, the efficiency of a data structure is closely tied to its concrete implementation, and must be evaluated through benchmarks and theoretical simulation.
Data structures generally rely on the ability of a computer to store and access data via memory addresses (as specified by a pointer—a bit string—or more abstractly via references) that can be itself stored in memory and manipulated by the program. For example, arrays and records store elements in contiguous memory locations, requiring a rigid layout but allowing fast indexed access by computing the address through arithmetic operations. In contrast, linked data structures (such as linked lists and trees) store addresses of related elements within their structure, enabling flexible memory usage and dynamic resizing. These different methods of data structuring come with different tradeoffs and are suited to different tasks. For instance, the contiguous memory allocation in arrays facilitates rapid access and modification operations, leading to optimized performance in sequential data processing scenarios.


== Examples ==

There are numerous types of data structures, generally built upon simpler primitive data types. Well known examples are:

An array is a number of elements in a specific order, typically all of the same type (depending on the language, individual elements may either all be forced to be the same type, or may be of almost any type). Elements are accessed using an integer index to specify which element is required. Typical implementations allocate contiguous memory words for the elements of arrays (but this is not always a necessity). Arrays may be fixed-length or resizable.
A linked list (also just called list) is a linear collection of data elements of any type, called nodes, where each node has itself a value, and points to the next node in the linked list. The principal advantage of a linked list over an array is that values can always be efficiently inserted and removed without relocating the rest of the list. Certain other operations, such as random access to a certain element, are however slower on lists than on arrays.
A record (also called tuple or struct) is an aggregate data structure. A record is a value that contains other values, typically in fixed number and sequence and typically indexed by names. The elements of records are usually called fields or members. In the context of object-oriented programming, records are known as plain old data structures to distinguish them from objects.
Hash tables, also known as hash maps, are data structures that provide fast retrieval of values based on keys. They use a hashing function to map keys to indexes in an array, allowing for constant-time access in the average case. Hash tables are commonly used in dictionaries, caches, and database indexing. However, hash collisions can occur, which can impact their performance. Techniques like chaining and open addressing are employed to handle collisions.
Graphs are collections of nodes connected by edges, representing relationships between entities. Graphs can be used to model social networks, computer networks, and transportation networks, among other things. They consist of vertices (nodes) and edges (connections between nodes). Graphs can be directed or undirected, and they can have cycles or be acyclic. Graph traversal algorithms include breadth-first search and depth-first search.
Stacks and queues are abstract data types that can be implemented using arrays or linked lists. A stack has two primary operations: push (adds an element to the top of the stack) and pop (removes the topmost element from the stack), that follow the Last In, First Out (LIFO) principle. Queues have two main operations: enqueue (adds an element to the rear of the queue) and dequeue (removes an element from the front of the queue) that follow the First In, First Out (FIFO) principle.
Trees represent a hierarchical organization of elements. A tree consists of nodes connected by edges, with one node being the root and all other nodes forming subtrees. Trees are widely used in various algorithms and data storage scenarios. Binary trees (particularly heaps), AVL trees, and B-trees are some popular types of trees. They enable efficient and optimal searching, sorting, and hierarchical representation of data.
A trie, or prefix tree, is a special type of tree used to efficiently retrieve strings. In a trie, each node represents a character of a string, and the edges between nodes represent the characters that connect them. This structure is especially useful for tasks like autocomplete, spell-checking, and creating dictionaries. Tries allow for quick searches and operations based on string prefixes.


== Language support ==
Most assembly languages and some low-level languages, such as BCPL (Basic Combined Programming Language), lack built-in support for data structures. On the other hand, many high-level programming languages and some higher-level assembly languages, such as MASM, have special syntax or other built-in support for certain data structures, such as records and arrays. For example, the C (a direct descendant of BCPL) and Pascal languages support structs and records, respectively, in addition to vectors (one-dimensional arrays) and multi-dimensional arrays.
Most programming languages feature some sort of library mechanism that allows data structure implementations to be reused by different programs. Modern languages usually come with standard libraries that implement the most common data structures. Examples are the C++ Standard Template Library, the Java Collections Framework, and the Microsoft .NET Framework.
Modern languages also generally support modular programming, the separation between the interface of a library module and its implementation. Some provide opaque data types that allow clients to hide implementation details.""",
    tier=9,
    domain="computer_science",
    source="Wikipedia, 'Data structure'",
    source_url="https://en.wikipedia.org/wiki/Data_structure",
))

register_atom(Atom(
    atom_type="methodology",
    name="training_diagnosis",
    content="""In mathematical modeling, overfitting is the production of an analysis that corresponds too closely or exactly to a particular set of data, and may therefore fail to fit to additional data or predict future observations reliably. An overfitted model is a mathematical model that contains more parameters than can be justified by the data. In the special case of a model that consists of a polynomial function, these parameters represent the degree of a polynomial. The essence of overfitting is to unknowingly extract some of the residual variation (i.e., noise) as if that variation represents the underlying model structure.
Underfitting occurs when a mathematical model cannot adequately capture the underlying structure of the data. An under-fitted model is a model that is missing some parameters or terms that would appear in a correctly specified model. Underfitting would occur, for example, when fitting a linear model to nonlinear data. Such a model will tend to have poor predictive performance.
The possibility of over-fitting exists when the criterion used for selecting the model is not the same as the criterion used to judge the suitability of a model. For example, a model might be selected by maximizing its performance on some set of training data, yet its suitability might be determined by its ability to perform well on unseen data; overfitting occurs when a model begins to "memorize" training data rather than "learning" to generalize from a trend.
As an extreme example, if the number of parameters is the same as or greater than the number of observations, then a model can perfectly predict the training data simply by memorizing the data in its entirety. (For an illustration, see Figure 2.) Such a model will typically fail severely when making predictions.
Overfitting is related to both the complexity of the chosen model and how well it is optimized during training. A function class that is too large, in a suitable sense, relative to the dataset size is likely to overfit. Even when the fitted model does not have an excessive number of parameters, it is to be expected that the fitted relationship will appear to perform less well on a new dataset than on the dataset used for fitting (a phenomenon sometimes known as shrinkage). In particular, the value of the coefficient of determination will shrink relative to the original data.
To lessen the chance or amount of overfitting, several techniques are available (e.g., model comparison, cross-validation, regularization, early stopping, pruning, Bayesian priors, or dropout). The basis of some techniques is to either (1) explicitly penalize overly complex models or (2) test the model's ability to generalize by evaluating its performance on a set of data not used for training, which is assumed to approximate the typical unseen data that a model will encounter.


== Statistical inference ==

In statistics, an inference is drawn from a statistical model, which has been selected via some procedure. Burnham & Anderson, in their much-cited text on model selection, argue that to avoid overfitting, one should adhere to the "Principle of Parsimony". The authors also state the following.

Overfitted models ... are often free of bias in the parameter estimators, but have estimated (and actual) sampling variances that are needlessly large (the precision of the estimators is poor, relative to what could have been accomplished with a more parsimonious model). False treatment effects tend to be identified, and false variables are included with overfitted models. ... A best approximating model is achieved by properly balancing the errors of underfitting and overfitting.
Overfitting is more likely to be a serious concern when there is little theory available to guide the analysis, in part because then there tend to be a large number of models to select from. The book Model Selection and Model Averaging (2008) puts it this way.

Given a data set, you can fit thousands of models at the push of a button, but how do you choose the best? With so many candidate models, overfitting is a real danger. Is the monkey who typed Hamlet actually a good writer?


=== Regression ===
In regression analysis, overfitting occurs frequently. As an extreme example, if there are p variables in a linear regression with p data points, the fitted line can go exactly through every point. For logistic regression or Cox proportional hazards models, there are a variety of rules of thumb (e.g. 5–9, 10 and 10–15 — the guideline of 10 observations per independent variable is known as the "one in ten rule"). In the process of regression model selection, the mean squared error of the random regression function can be split into random noise, approximation bias, and variance in the estimate of the regression function. The bias–variance tradeoff is often used to overcome overfit models.
With a large set of explanatory variables that actually have no relation to the dependent variable being predicted, some variables will in general be falsely found to be statistically significant and the researcher may thus retain them in the model, thereby overfitting the model. This is known as Freedman's paradox.


== Machine learning ==

Usually, a learning algorithm is trained using some set of "training data": exemplary situations for which the desired output is known. The goal is that the algorithm will also perform well on predicting the output when fed "validation data" that was not encountered during its training.
Overfitting is the use of models or procedures that violate Occam's razor, for example by including more adjustable parameters than are ultimately optimal, or by using a more complicated approach than is ultimately optimal. For an example where there are too many adjustable parameters, consider a dataset where training data for y can be adequately predicted by a linear function of two independent variables. Such a function requires only three parameters (the intercept and two slopes). Replacing this simple function with a new, more complex quadratic function, or with a new, more complex linear function on more than two independent variables, carries a risk: Occam's razor implies that any given complex function is a priori less probable than any given simple function. If the new, more complicated function is selected instead of the simple function, and if there was not a large enough gain in training data fit to offset the complexity increase, then the new complex function "overfits" the data and the complex overfitted function will likely perform worse than the simpler function on validation data outside the training dataset, even though the complex function performed as well, or perhaps even better, on the training dataset.
When comparing different types of models, complexity cannot be measured solely by counting how many parameters exist in each model; the expressivity of each parameter must be considered as well. For example, it is nontrivial to directly compare the complexity of a neural net (which can track curvilinear relationships) with m parameters to a regression model with n parameters.
Overfitting is especially likely in cases where learning was performed too long or where training examples are rare, causing the learner to adjust to very specific random features of the training data that have no causal relation to the target function. In this process of overfitting, the performance on the training examples still increases while the performance on unseen data becomes worse.
As a simple example, consider a database of retail purchases that includes the item bought, the purchaser, and the date and time of purchase.""",
    tier=10,
    domain="deep_learning",
    source="Wikipedia, 'Overfitting'",
    source_url="https://en.wikipedia.org/wiki/Overfitting",
))

register_atom(Atom(
    atom_type="methodology",
    name="failure_mode_classification",
    content="""Failure mode and effects analysis (FMEA; often written with "failure modes" in plural) is the process of reviewing as many components, assemblies, and subsystems as possible to identify potential failure modes in a system and their causes and effects. For each component, the failure modes and their resulting effects on the rest of the system are recorded in a specific FMEA worksheet. There are numerous variations of such worksheets. A FMEA can be a qualitative analysis, but may be put on a semi-quantitative basis with an RPN (Risk Priority Number) model. Related methods combine mathematical failure rate models with statistical failure mode ratio databases. It was one of the first highly structured, systematic techniques for failure analysis. It was developed by reliability engineers in the late 1950s to study problems that might arise from malfunctions of military systems. An FMEA is often the first step of a system reliability study.
A few different types of FMEA analyses exist, such as:

Functional
Design
Process
Software
Sometimes FMEA is extended to FMECA(failure mode, effects, and criticality analysis) with Risk Priority Numbers (RPN) to indicate criticality.  
FMEA is an inductive reasoning (forward logic) single point of failure analysis and is a core task in reliability engineering, safety engineering and quality engineering.
A successful FMEA activity helps identify potential failure modes based on experience with similar products and processes—or based on common physics of failure logic. It is widely used in development and manufacturing industries in various phases of the product life cycle. Effects analysis refers to studying the consequences of those failures on different system levels.
Functional analyses are needed as an input to determine correct failure modes, at all system levels, both for functional FMEA or piece-part (hardware) FMEA. An FMEA is used to structure mitigation for risk reduction based on either reducing the severity of the failure mode or effect, or on lowering the probability of failure, or both. 
The FMEA is in principle a full inductive (forward logic) analysis; however the failure probability can only be estimated or reduced by understanding the failure mechanism. Hence, FMEA may include information on causes of failure (deductive analysis) to reduce the possibility of occurrence by eliminating identified (root) causes.


== Introduction ==
The FME(C)A is a design tool used to systematically analyze postulated component failures and identify the resultant effects on system operations. The analysis is sometimes characterized as consisting of two sub-analyses, the first being the failure modes and effects analysis (FMEA), and the second, the criticality analysis (CA). Successful development of an FMEA requires that the analyst include all significant failure modes for each contributing element or part in the system. FMEAs can be performed at the system, subsystem, assembly, subassembly or part level. 
The FMECA should be a living document during development of a hardware design. It should be scheduled and completed concurrently with the design. If completed in a timely manner, the FMECA can help guide design decisions. The usefulness of the FMECA as a design tool and in the decision-making process is dependent on the effectiveness and timeliness with which design problems are identified. Timeliness is probably the most important consideration. In the extreme case, the FMECA would be of little value to the design decision process if the analysis is performed after the hardware is built. While the FMECA identifies all part failure modes, its primary benefit is the early identification of all critical and catastrophic subsystem or system failure modes so they can be eliminated or minimized through design modification at the earliest point in the development effort; therefore, the FMECA should be performed at the system level as soon as preliminary design information is available and extended to the lower levels as the detail design progresses.
Remark: For more complete scenario modelling another type of reliability analysis may be considered, for example fault tree analysis (FTA); a deductive (backward logic) failure analysis that may handle multiple failures within the item and/or external to the item including maintenance and logistics. It starts at higher functional / system level. An FTA may use the basic failure mode FMEA records or an effect summary as one of its inputs (the basic events). Interface hazard analysis, human error analysis and others may be added for completion in scenario modelling.


=== Functional failure mode and effects analysis ===
The analysis should always be started by someone listing the functions that the design needs to fulfill. Functions are the starting point of a well done FMEA, and using functions as baseline provides the best yield of an FMEA. After all, a design is only one possible solution to perform functions that need to be fulfilled. This way an FMEA can be done on concept designs as well as detail designs, on hardware as well as software, and no matter how complex the design.
When performing a FMECA, interfacing hardware (or software) is first considered to be operating within specification. After that it can be extended by consequently using one of the 5 possible failure modes of one function of the interfacing hardware as a cause of failure for the design element under review. This gives the opportunity to make the design robust against function failure elsewhere in the system.
In addition, each part failure postulated is considered to be the only failure in the system (i.e., it is a single failure analysis). In addition to the FMEAs done on systems to evaluate the impact lower level failures have on system operation, several other FMEAs are done. Special attention is paid to interfaces between systems and in fact at all functional interfaces. The purpose of these FMEAs is to assure that irreversible physical and/or functional damage is not propagated across the interface as a result of failures in one of the interfacing units. These analyses are done to the piece part level for the circuits that directly interface with the other units. The FMEA can be accomplished without a CA, but a CA requires that the FMEA has previously identified system level critical failures. When both steps are done, the total process is called an FMECA.


=== Ground rules ===
The ground rules of each FMEA include a set of project selected procedures; the assumptions on which the analysis is based; the hardware that has been included and excluded from the analysis; and the rationale for the exclusions. The ground rules also describe the indenture level of the analysis (i.e. the level in the hierarchy of the part to the sub-system, sub-system to the system, etc.), the basic hardware status, and the criteria for system and mission success. Every effort should be made to define all ground rules before the FMEA begins; however, the ground rules may be expanded and clarified as the analysis proceeds. A typical set of ground rules (assumptions) follows:

Only one failure mode exists at a time.
All inputs (including software commands) to the item being analyzed are present and at nominal values.
All consumables are present in sufficient quantities.
Nominal power is available.


=== Benefits ===
Major benefits derived from a properly implemented FMECA effort are as follows. It provides: 

A documented method for selecting a design with a high probability of successful operation and safety.
A documented uniform method of assessing potential failure mechanisms, failure modes and their impact on system operation, resulting in a list of failure modes ranked according to the seriousness of their system impact and likelihood of occurrence.
Early identification of single failure points (SFPS) and system interface problems, which may be critical to mission success and/or safety.""",
    tier=10,
    domain="deep_learning",
    source="Wikipedia, 'Failure mode and effects analysis'",
    source_url="https://en.wikipedia.org/wiki/Failure_mode_and_effects_analysis",
))

register_atom(Atom(
    atom_type="methodology",
    name="data_prescription",
    content="""In machine learning, a common task is the study and construction of algorithms that can learn from and make predictions on data. Such algorithms function by making data-driven predictions or decisions, through building a mathematical model from input data. These input data used to build the model are usually divided into multiple data sets. In particular, three data sets are commonly used in different stages of the creation of the model: training, validation, and testing sets.
The model is initially fit on a training data set, which is a set of examples used to fit the parameters (e.g. weights of connections between neurons in artificial neural networks) of the model. The model (e.g. a naive Bayes classifier) is trained on the training data set using a supervised learning method, for example using optimization methods such as gradient descent or stochastic gradient descent. In practice, the training data set often consists of pairs of an input vector (or scalar) and the corresponding output vector (or scalar), where the answer key is commonly denoted as the target (or label). The current model is run with the training data set and produces a result, which is then compared with the target, for each input vector in the training data set. Based on the result of the comparison and the specific learning algorithm being used, the parameters of the model are adjusted. The model fitting can include both variable selection and parameter estimation.
Successively, the fitted model is used to predict the responses for the observations in a second data set called the validation data set. The validation data set provides an unbiased evaluation of a model fit on the training data set while tuning the model's hyperparameters (e.g. the number of hidden units—layers and layer widths—in a neural network). Validation data sets can be used for regularization by early stopping (stopping training when the error on the validation data set increases, as this is a sign of over-fitting to the training data set).
This simple procedure is complicated in practice by the fact that the validation data set's error may fluctuate during training, producing multiple local minima. This complication has led to the creation of many ad-hoc rules for deciding when over-fitting has truly begun.
Finally, the test data set is a data set used to provide an unbiased evaluation of a model fit on the training data set. When the data in the test data set has never been used (for example in cross-validation), the test data set is called a holdout data set. The term "validation set" is sometimes used instead of "test set" in some literature (e.g., if the original data set was partitioned into only two subsets, the test set might be referred to as the validation set).
Deciding the sizes and strategies for data set division in training, test and validation sets is very dependent on the problem and data available.


== Training data set ==

A training data set is a data set of examples used during the learning process and is used to fit the parameters (e.g., weights) of, for example, a classifier.
For classification tasks, a supervised learning algorithm looks at the training data set to determine, or learn, the optimal combinations of variables that will generate a good predictive model. The goal is to produce a trained (fitted) model that generalizes well to new, unknown data. The fitted model is evaluated using “new” examples from the held-out data sets (validation and test data sets) to estimate the model’s accuracy in classifying new data. To reduce the risk of issues such as over-fitting, the examples in the validation and test data sets should not be used to train the model.
Most approaches that search through training data for empirical relationships tend to overfit the data, meaning that they can identify and exploit apparent relationships in the training data that do not hold in general.
When a training set is continuously expanded with new data, then this is incremental learning.


== Validation data set ==
A validation data set is a data set of examples used to tune the hyperparameters (i.e. the architecture) of a model. It is sometimes also called the development set or the "dev set". An example of a hyperparameter for artificial neural networks includes the number of hidden units in each layer. It, as well as the testing set (as mentioned below), should follow the same probability distribution as the training data set.
In order to avoid overfitting, when any classification parameter needs to be adjusted, it is necessary to have a validation data set in addition to the training and test data sets. For example, if the most suitable classifier for the problem is sought, the training data set is used to train the different candidate classifiers, the validation data set is used to compare their performances and decide which one to take and, finally, the test data set is used to obtain the performance characteristics such as accuracy, sensitivity, specificity, F-measure, and so on. The validation data set functions as a hybrid: it is training data used for testing, but neither as part of the low-level training nor as part of the final testing.
The basic process of using a validation data set for model selection (as part of training data set, validation data set, and test data set) is:

Since our goal is to find the network having the best performance on new data, the simplest approach to the comparison of different networks is to evaluate the error function using data which is independent of that used for training. Various networks are trained by minimization of an appropriate error function defined with respect to a training data set. The performance of the networks is then compared by evaluating the error function using an independent validation set, and the network having the smallest error with respect to the validation set is selected. This approach is called the hold out method. Since this procedure can itself lead to some overfitting to the validation set, the performance of the selected network should be confirmed by measuring its performance on a third independent set of data called a test set.
An application of this process is in early stopping, where the candidate models are successive iterations of the same network, and training stops when the error on the validation set grows, choosing the previous model (the one with minimum error).


== Test data set ==
A test data set is a data set that is independent of the training data set, but that follows the same probability distribution as the training data set. A test set is therefore a set of examples used only to assess the performance (i.e. generalization) of a specified classifier on unseen data. To do this, the model is used to predict classifications of examples in the test set. Those predictions are compared to the examples' true classifications to assess the model's accuracy. If a model fit to the training and validation data set also fits the test data set well, minimal overfitting has taken place (see figure below). A better fitting of the training or validation data sets as opposed to the test data set usually points to overfitting.
In the scenario where a data set has a low number of samples, it is usually partitioned into a training set and a validation data set, where the model is trained on the training set and refined using the validation set to improve accuracy, but this approach will lead to overfitting. The holdout method can also be employed, where the test set is used at the end, after training on the training set. Other techniques, such as cross-validation and  bootstrapping, are used on small data sets. The bootstrap method generates numerous simulated data sets of the same size by randomly sampling with replacement from the original data, allowing the random data points to serve as test sets for evaluating model performance.""",
    tier=10,
    domain="deep_learning",
    source="Wikipedia, 'Training, validation, and test data sets'",
    source_url="https://en.wikipedia.org/wiki/Training%2C_validation%2C_and_test_data_sets",
))

register_atom(Atom(
    atom_type="principle",
    name="efficiency_analysis",
    content="""In computer science, algorithmic efficiency is a property of an algorithm which relates to the amount of computational resources used by the algorithm. Algorithmic efficiency can be thought of as analogous to engineering productivity for a repeating or continuous process.
For maximum efficiency it is desirable to minimize resource usage. However, different resources such as time and space complexity cannot be compared directly, so which of two algorithms is considered to be more efficient often depends on which measure of efficiency is considered most important.
For example, cycle sort and Timsort are both algorithms to sort a list of items from smallest to largest. Cycle sort organizes the list in time proportional to the number of elements squared (
  
    
      
        O
        (
        
          n
          
            2
          
        
        )
      
    
    {\\textstyle O(n^{2})}
  
, see big O notation), but minimizes the writes to the original array and only requires a small amount of extra memory which is constant with respect to the length of the list (
  
    
      
        O
        (
        1
        )
      
    
    {\\textstyle O(1)}
  
). Timsort sorts the list in time linearithmic (proportional to a quantity times its logarithm) in the list's length (
  
    
      
        O
        (
        n
        log
        ⁡
        n
        )
      
    
    {\\textstyle O(n\\log n)}
  
), but has a space requirement linear in the length of the list (
  
    
      
        O
        (
        n
        )
      
    
    {\\textstyle O(n)}
  
). If large lists must be sorted at high speed for a given application, timsort is a better choice; however, if minimizing the program/erase cycles and memory footprint of the sorting is more important, cycle sort is a better choice.


== Background ==
The importance of efficiency with respect to time was emphasized by Ada Lovelace in 1843 as applied to Charles Babbage's mechanical analytical engine:

"In almost every computation a great variety of arrangements for the succession of the processes is possible, and various considerations must influence the selections amongst them for the purposes of a calculating engine. One essential object is to choose that arrangement which shall tend to reduce to a minimum the time necessary for completing the calculation"
Early electronic computers had both limited speed and limited random-access memory. Therefore, a space–time trade-off occurred. A task could use a fast algorithm using a lot of memory, or it could use a slow algorithm using little memory. The engineering trade-off was therefore to use the fastest algorithm that could fit in the available memory.
Modern computers are significantly faster than early computers and have a much larger amount of memory available (gigabytes instead of kilobytes). Nevertheless, Donald Knuth emphasized that efficiency is still an important consideration:

 "In established engineering disciplines a 12% improvement, easily obtained, is never considered marginal and I believe the same viewpoint should prevail in software engineering"In the era of AI, while LLMs can generate code that works, these often fall short of the performance standards required in resource-constrained or time-sensitive applications, making code efficiency a critical bottleneck for real-world deployment.


== Overview ==
An algorithm is considered efficient if its resource consumption, also known as computational cost, is at or below some acceptable level. Roughly speaking, 'acceptable' means:  it will run in a reasonable amount of time or space on an available computer, typically as a function of the size of the input. Since the 1950s computers have seen dramatic increases in both the available computational power and in the available amount of memory, so current acceptable levels would have been unacceptable even 10 years ago. In fact, thanks to the approximate doubling of computer power every 2 years, tasks that are acceptably efficient on modern smartphones and embedded systems may have been unacceptably inefficient for industrial servers 10 years ago.
Computer manufacturers frequently bring out new models, often with higher performance. Software costs can be quite high, so in some cases the simplest and cheapest way of getting higher performance might be to just buy a faster computer, provided it is compatible with an existing computer.
There are many ways in which the resources used by an algorithm can be measured: the two most common measures are speed and memory usage; other measures could include transmission speed, temporary disk usage, long-term disk usage, power consumption, total cost of ownership, response time to external stimuli, etc. Many of these measures depend on the size of the input to the algorithm, i.e. the amount of data to be processed. They might also depend on the way in which the data is arranged; for example, some sorting algorithms perform poorly on data which is already sorted, or which is sorted in reverse order.
In practice, there are other factors which can affect the efficiency of an algorithm, such as requirements for accuracy and/or reliability. As detailed below, the way in which an algorithm is implemented can also have a significant effect on actual efficiency, though many aspects of this relate to optimization issues.


=== Theoretical analysis ===
In the theoretical analysis of algorithms, the normal practice is to estimate their complexity in the asymptotic sense. The most commonly used notation to describe resource consumption or "complexity" is Donald Knuth's Big O notation, representing the complexity of an algorithm as a function of the size of the input 
  
    
      
        n
      
    
    {\\textstyle n}
  
. Big O notation is an asymptotic measure of function complexity, where 
  
    
      
        f
        (
        n
        )
        =
        O
        
          
            (
          
        
        g
        (
        n
        )
        
          
            )
          
        
      
    
    {\\textstyle f(n)=O{\\bigl (}g(n){\\bigr )}}
  
 roughly means the time requirement for an algorithm is proportional to 
  
    
      
        g
        (
        n
        )
      
    
    {\\displaystyle g(n)}
  
, omitting lower-order terms that contribute less than 
  
    
      
        g
        (
        n
        )
      
    
    {\\displaystyle g(n)}
  
 to the growth of the function as 
  
    
      
        n
      
    
    {\\textstyle n}
  
 grows arbitrarily large. This estimate may be misleading when 
  
    
      
        n
      
    
    {\\textstyle n}
  
 is small, but is generally sufficiently accurate when 
  
    
      
        n
      
    
    {\\textstyle n}
  
 is large as the notation is asymptotic. For example, bubble sort may be faster than merge sort when only a few items are to be sorted; however either implementation is likely to meet performance requirements for a small list. Typically, programmers are interested in algorithms that scale efficiently to large input sizes, and merge sort is preferred over bubble sort for lists of length encountered in most data-intensive programs.
Some examples of Big O notation applied to algorithms' asymptotic time complexity include:


=== Measuring performance ===
For new versions of software or to provide comparisons with competitive systems, benchmarks are sometimes used, which assist with gauging an algorithms relative performance. If a new sort algorithm is produced, for example, it can be compared with its predecessors to ensure that at least it is efficient as before with known data, taking into consideration any functional improvements. Benchmarks can be used by customers when comparing various products from alternative suppliers to estimate which product will best suit their specific requirements in terms of functionality and performance.""",
    tier=10,
    domain="deep_learning",
    source="Wikipedia, 'Algorithmic efficiency'",
    source_url="https://en.wikipedia.org/wiki/Algorithmic_efficiency",
))

register_atom(Atom(
    atom_type="result",
    name="emergent_capability",
    content="""In philosophy, systems theory, science, and art, emergence occurs when a complex entity has properties or behaviors that its parts do not have on their own, and emerge only when they interact in a wider whole.
Emergence plays a central role in theories of integrative levels and of complex systems. For instance, the phenomenon of life as studied in biology is an emergent property of chemistry and physics.


== In philosophy ==

Philosophers often understand emergence as a claim about the etiology of a system's properties. An emergent property of a system, in this context, is one that is not a property of any component of that system, but is still a feature of the system as a whole. Nicolai Hartmann (1882–1950), one of the first modern philosophers to write on emergence, termed this a categorial novum (new category).


=== Definitions ===
This concept of emergence dates from at least the time of Aristotle. In Heideggerian thought, the notion of emergence is derived from the Greek word poiein, meaning "to make", and refers to a bringing-forth that encompasses not just a process of crafting (techne) but also the broader sense of something coming into being or revealing itself. Heidegger used emerging blossoms and butterflies as examples to illustrate poiêsis as a threshold event where something moves from one state to another. Many scientists and philosophers  have written on the concept, including John Stuart Mill (Composition of Causes, 1843) and Julian Huxley (1887–1975).
The philosopher G. H. Lewes coined the term "emergent" in 1875, distinguishing it from the merely "resultant":

Every resultant is either a sum or a difference of the co-operant forces; their sum, when their directions are the same – their difference, when their directions are contrary. Further, every resultant is clearly traceable in its components, because these are homogeneous and commensurable. It is otherwise with emergents, when, instead of adding measurable motion to measurable motion, or things of one kind to other individuals of their kind, there is a co-operation of things of unlike kinds. The emergent is unlike its components insofar as these are incommensurable, and it cannot be reduced to their sum or their difference.


=== Strong and weak emergence ===

Usage of the notion "emergence" may generally be subdivided into two perspectives, that of "weak emergence" and "strong emergence". One paper discussing this division is Weak Emergence, by philosopher Mark Bedau. In terms of physical systems, weak emergence is a type of emergence in which the emergent property is amenable to computer simulation or similar forms of after-the-fact analysis (for example, the formation of a traffic jam, the structure of a flock of starlings in flight or a school of fish, or the formation of galaxies). Crucial in these simulations is that the interacting members retain their independence. If not, a new entity is formed with new, emergent properties: this is called strong emergence, which it is argued cannot be simulated, analysed or reduced.
David Chalmers writes that emergence often causes confusion in philosophy and science due to a failure to demarcate strong and weak emergence, which are "quite different concepts".
Some common points between the two notions are that emergence concerns new properties produced as the system grows, which is to say ones which are not shared with its components or prior states. Also, it is assumed that the properties are supervenient rather than metaphysically primitive.
Weak emergence describes new properties arising in systems as a result of the interactions at a fundamental level. However, Bedau stipulates that the properties can be determined only by observing or simulating the system, and not by any process of a reductionist analysis. As a consequence the emerging properties are scale dependent: they are only observable if the system is large enough to exhibit the phenomenon. Chaotic, unpredictable behaviour can be seen as an emergent phenomenon, while at a microscopic scale the behaviour of the constituent parts can be fully deterministic.
Bedau notes that weak emergence is not a universal metaphysical solvent, as the hypothesis that consciousness is weakly emergent would not resolve the traditional philosophical questions about the physicality of consciousness. However, Bedau concludes that adopting this view would provide a precise notion that emergence is involved in consciousness, and second, the notion of weak emergence is metaphysically benign.
Strong emergence describes the direct causal action of a high-level system on its components; qualities produced this way are irreducible to the system's constituent parts. The whole is other than the sum of its parts. It is argued then that no simulation of the system can exist, for such a simulation would itself constitute a reduction of the system to its constituent parts. Physics lacks well-established examples of strong emergence, unless it is interpreted as the impossibility in practice to explain the whole in terms of the parts. Practical impossibility may be a more useful distinction than one in principle, since it is easier to determine and quantify, and does not imply the use of mysterious forces, but simply reflects the limits of our capability.


==== Viability of strong emergence ====
One of the reasons for the importance of distinguishing these two concepts with respect to their difference concerns the relationship of purported emergent properties to science. Some thinkers question the plausibility of strong emergence as contravening our usual understanding of physics. Mark A. Bedau observes:

Although strong emergence is logically possible, it is uncomfortably like magic. How does an irreducible but supervenient downward causal power arise, since by definition it cannot be due to the aggregation of the micro-level potentialities? Such causal powers would be quite unlike anything within our scientific ken. This not only indicates how they will discomfort reasonable forms of materialism. Their mysteriousness will only heighten the traditional worry that emergence entails illegitimately getting something from nothing.
The concern that strong emergence does so entail is that such a consequence must be incompatible with metaphysical principles such as the principle of sufficient reason or the Latin dictum ex nihilo nihil fit, often translated as "nothing comes from nothing".
Strong emergence can be criticized for leading to causal overdetermination. The canonical example concerns emergent mental states (M and M∗) that supervene on physical states (P and P∗) respectively. Let M and M∗ be emergent properties. Let M∗ supervene on base property P∗. What happens when M causes M∗? Jaegwon Kim says:

In our schematic example above, we concluded that M causes M∗ by causing P∗. So M causes P∗. Now, M, as an emergent, must itself have an emergence base property, say P. Now we face a critical question: if an emergent, M, emerges from basal condition P, why cannot P displace M as a cause of any putative effect of M? Why cannot P do all the work in explaining why any alleged effect of M occurred? If causation is understood as nomological (law-based) sufficiency, P, as M's emergence base, is nomologically sufficient for it, and M, as P∗'s cause, is nomologically sufficient for P∗. It follows that P is nomologically sufficient for P∗ and hence qualifies as its cause...If M is somehow retained as a cause, we are faced with the highly implausible consequence that every case of downward causation involves overdetermination (since P remains a cause of P∗ as well). Moreover, this goes against the spirit of emergentism in any case: emergents are supposed to make distinctive and novel causal contributions.
If M is the cause of M∗, then M∗ is overdetermined because M∗ can also be thought of as being determined by P. One escape-route that a strong emergentist could take would be to deny downward causation.""",
    tier=10,
    domain="deep_learning",
    source="Wikipedia, 'Emergence'",
    source_url="https://en.wikipedia.org/wiki/Emergence",
))

register_atom(Atom(
    atom_type="principle",
    name="capacity_bound",
    content="""Channel capacity, in electrical engineering, computer science, and information theory, is the theoretical maximum rate at which information can be reliably transmitted over a communication channel.
Following the terms of the noisy-channel coding theorem, the channel capacity of a given channel is the highest information rate (in units of information per unit time) that can be achieved with arbitrarily small error probability.
Information theory, developed by Claude E. Shannon in 1948, defines the notion of channel capacity and provides a mathematical model by which it may be computed. The key result states that the capacity of the channel, as defined above, is given by the maximum of the mutual information between the input and output of the channel, where the maximization is with respect to the input distribution.
The notion of channel capacity has been central to the development of modern wireline and wireless communication systems, with the advent of novel error correction coding mechanisms that have resulted in achieving performance very close to the limits promised by channel capacity.


== Formal definition ==
The basic mathematical model for a communication system is the following:

  
    
      
        
          
            →
            
              
                Message
              
            
            
              W
            
          
        
        
          
            
              
                
                  Encoder
                
              
            
            
              
                
                  f
                  
                    n
                  
                
              
            
          
        
        
          
            →
            
              
                
                  
                    
                      E
                      n
                      c
                      o
                      d
                      e
                      d
                    
                    
                      s
                      e
                      q
                      u
                      e
                      n
                      c
                      e
                    
                  
                
              
            
            
              
                X
                
                  n
                
              
            
          
        
        
          
            
              
                
                  Channel
                
              
            
            
              
                p
                (
                y
                
                  |
                
                x
                )
              
            
          
        
        
          
            →
            
              
                
                  
                    
                      R
                      e
                      c
                      e
                      i
                      v
                      e
                      d
                    
                    
                      s
                      e
                      q
                      u
                      e
                      n
                      c
                      e
                    
                  
                
              
            
            
              
                Y
                
                  n
                
              
            
          
        
        
          
            
              
                
                  Decoder
                
              
            
            
              
                
                  g
                  
                    n
                  
                
              
            
          
        
        
          
            →
            
              
                
                  
                    
                      E
                      s
                      t
                      i
                      m
                      a
                      t
                      e
                      d
                    
                    
                      m
                      e
                      s
                      s
                      a
                      g
                      e
                    
                  
                
              
            
            
              
                
                  W
                  ^
                
              
            
          
        
      
    
    {\\displaystyle {\\xrightarrow[{\\text{Message}}]{W}}{\\begin{array}{|c|}\\hline {\\text{Encoder}}\\\\f_{n}\\\\\\hline \\end{array}}{\\xrightarrow[{\\mathrm {Encoded \\atop sequence} }]{X^{n}}}{\\begin{array}{|c|}\\hline {\\text{Channel}}\\\\p(y|x)\\\\\\hline \\end{array}}{\\xrightarrow[{\\mathrm {Received \\atop sequence} }]{Y^{n}}}{\\begin{array}{|c|}\\hline {\\text{Decoder}}\\\\g_{n}\\\\\\hline \\end{array}}{\\xrightarrow[{\\mathrm {Estimated \\atop message} }]{\\hat {W}}}}
  

where:

  
    
      
        W
      
    
    {\\displaystyle W}
  
 is the message to be transmitted;

  
    
      
        X
      
    
    {\\displaystyle X}
  
 is the channel input symbol (
  
    
      
        
          X
          
            n
          
        
      
    
    {\\displaystyle X^{n}}
  
 is a sequence of 
  
    
      
        n
      
    
    {\\displaystyle n}
  
 symbols) taken in an alphabet 
  
    
      
        
          
            X
          
        
      
    
    {\\displaystyle {\\mathcal {X}}}
  
;

  
    
      
        Y
      
    
    {\\displaystyle Y}
  
 is the channel output symbol (
  
    
      
        
          Y
          
            n
          
        
      
    
    {\\displaystyle Y^{n}}
  
 is a sequence of 
  
    
      
        n
      
    
    {\\displaystyle n}
  
 symbols) taken in an alphabet 
  
    
      
        
          
            Y
          
        
      
    
    {\\displaystyle {\\mathcal {Y}}}
  
;

  
    
      
        
          
            
              W
              ^
            
          
        
      
    
    {\\displaystyle {\\hat {W}}}
  
 is the estimate of the transmitted message;

  
    
      
        
          f
          
            n
          
        
      
    
    {\\displaystyle f_{n}}
  
 is the encoding function for a block of length 
  
    
      
        n
      
    
    {\\displaystyle n}
  
;

  
    
      
        p
        (
        y
        
          |
        
        x
        )
        =
        
          p
          
            Y
            
              |
            
            X
          
        
        (
        y
        
          |
        
        x
        )
      
    
    {\\displaystyle p(y|x)=p_{Y|X}(y|x)}
  
 is the noisy channel, which is modeled by a conditional probability distribution; and,

  
    
      
        
          g
          
            n
          
        
      
    
    {\\displaystyle g_{n}}
  
 is the decoding function for a block of length 
  
    
      
        n
      
    
    {\\displaystyle n}
  
.
Let 
  
    
      
        X
      
    
    {\\displaystyle X}
  
 and 
  
    
      
        Y
      
    
    {\\displaystyle Y}
  
 be modeled as random variables.""",
    tier=10,
    domain="information_theory",
    source="Wikipedia, 'Channel capacity'",
    source_url="https://en.wikipedia.org/wiki/Channel_capacity",
))

register_atom(Atom(
    atom_type="methodology",
    name="loss_design",
    content="""In mathematical optimization and decision theory, a loss function or cost function (sometimes also called an error function) is a function that maps an event or values of one or more variables onto a real number intuitively representing some "cost" associated with the event. An optimization problem seeks to minimize a loss function. An objective function is either a loss function or its opposite (in specific domains, variously called a reward function, a profit function, a utility function, a fitness function, etc.), in which case it is to be maximized. The loss function could include terms from several levels of the hierarchy.
In statistics, typically a  loss function is used for parameter estimation, and the event in question is some function of the difference between estimated and true values for an instance of data. The concept, as old as Laplace, was reintroduced in statistics by Abraham Wald in the middle of the 20th century.  In the context of economics, for example, this is usually economic cost or regret.  In classification, it is the penalty for an incorrect classification of an example. In actuarial science, it is used in an insurance context to model benefits paid over premiums, particularly since the works of Harald Cramér in the 1920s. In optimal control, the loss is the penalty for failing to achieve a desired value. In financial risk management, the function is mapped to a monetary loss.


== Examples ==


=== Regret ===

Leonard J. Savage argued that using non-Bayesian methods such as minimax, the loss function should be based on the idea of regret, i.e., the loss associated with a decision should be the difference between the consequences of the best decision that could have been made under circumstances will be known and the decision that was in fact taken before they were known.


=== Quadratic loss function ===
The use of a quadratic loss function is common, for example when using least squares techniques. It is often more mathematically tractable than other loss functions because of the properties of variances, as well as being symmetric: an error above the target causes the same loss as the same magnitude of error below the target.  If the target is 
  
    
      
        t
      
    
    {\\displaystyle t}
  
, then a quadratic loss function is

  
    
      
        λ
        (
        x
        )
        =
        C
        (
        t
        −
        x
        
          )
          
            2
          
        
        
      
    
    {\\displaystyle \\lambda (x)=C(t-x)^{2}\\;}
  

for some constant 
  
    
      
        C
      
    
    {\\displaystyle C}
  
; the value of the constant makes no difference to a decision, and can be ignored by setting it equal to 1. This is also known as the squared error loss (SEL).
Many common statistics, including t-tests, regression models, design of experiments, and much else, use least squares methods applied using linear regression theory, which is based on the quadratic loss function.
The quadratic loss function is also used in linear-quadratic optimal control problems. In these problems, even in the absence of uncertainty, it may not be possible to achieve the desired values of all target variables. Often loss is expressed as a quadratic form in the deviations of the variables of interest from their desired values; this approach is tractable because it results in linear first-order conditions. In the context of stochastic control, the expected value of the quadratic form is used. The quadratic loss assigns more importance to outliers than to the true data due to its square nature, so alternatives like the Huber, log-cosh and SMAE losses are used when the data has many large outliers.


=== 0-1 loss function ===
In statistics and decision theory, a frequently used loss function is the 0-1 loss function

  
    
      
        L
        (
        
          
            
              y
              ^
            
          
        
        ,
        y
        )
        =
        
          
            {
            
              
                
                  0
                
                
                  
                    if 
                  
                  y
                  =
                  
                    
                      
                        y
                        ^
                      
                    
                  
                
              
              
                
                  1
                
                
                  
                    if 
                  
                  y
                  ≠
                  
                    
                      
                        y
                        ^
                      
                    
                  
                
              
            
            
          
        
      
    
    {\\displaystyle L({\\hat {y}},y)={\\begin{cases}0&{\\text{if }}y={\\hat {y}}\\\\1&{\\text{if }}y\\neq {\\hat {y}}\\end{cases}}}
  

In information theory, this loss function is known as Hamming distortion.


== Constructing loss and objective functions ==

In many applications, objective functions, including loss functions as a particular case, are determined by the problem formulation.  In other situations, the decision maker’s preference must be elicited and represented by a scalar-valued function (called also  utility function) in a form  suitable for optimization — the problem that Ragnar Frisch has highlighted in his Nobel Prize lecture.
The existing methods for constructing objective functions are collected in the proceedings of two dedicated conferences.
In particular, Andranik Tangian showed that the most usable objective functions — quadratic and additive — are determined by a few indifference points. He used this property in the models for constructing these objective functions from either ordinal or cardinal data that were elicited through computer-assisted interviews with decision makers. 
Among other things, he constructed  objective functions to optimally distribute budgets for 16 Westfalian universities
and the European subsidies for equalizing unemployment rates among 271 German regions.


== Expected loss ==

In some contexts, the value of the loss function itself is a random quantity because it depends on the outcome of a random variable 
  
    
      
        X
      
    
    {\\displaystyle X}
  
. 


=== Statistics ===
Both frequentist and Bayesian statistical theory involve making a decision based on the expected value of the loss function; however, this quantity is defined differently under the two paradigms.


==== Frequentist expected loss ====
We first define the expected loss in the frequentist context. It is obtained by taking the expected value with respect to the probability distribution, 
  
    
      
        
          P
          
            θ
          
        
      
    
    {\\displaystyle P_{\\theta }}
  
, of the observed data, 
  
    
      
        X
      
    
    {\\displaystyle X}
  
. This is also referred to as the risk function of the decision rule 
  
    
      
        δ
      
    
    {\\displaystyle \\delta }
  
 and the parameter 
  
    
      
        θ
      
    
    {\\displaystyle \\theta }
  
. Here the decision rule depends on the outcome of 
  
    
      
        X
      
    
    {\\displaystyle X}
  
.""",
    tier=10,
    domain="deep_learning",
    source="Wikipedia, 'Loss function'",
    source_url="https://en.wikipedia.org/wiki/Loss_function",
))

register_atom(Atom(
    atom_type="principle",
    name="architecture_analysis",
    content="""The following tables list the computational complexity of various algorithms for common mathematical operations.
Here, complexity refers to the time complexity of performing computations on a multitape Turing machine. See big O notation for an explanation of the notation used.
Note: Due to the variety of multiplication algorithms, 
  
    
      
        M
        (
        n
        )
      
    
    {\\displaystyle M(n)}
  
 below stands in for the complexity of the chosen multiplication algorithm.


== Arithmetic functions ==
This table lists the complexity of mathematical operations on integers.

On stronger computational models, specifically a pointer machine and consequently also a unit-cost random-access machine it is possible to multiply two n-bit numbers in time O(n).


== Algebraic functions ==
Here we consider operations over polynomials and n denotes their degree; for the coefficients we use a unit-cost model, ignoring the number of bits in a number. In practice this means that we assume them to be machine integers. For this section 
  
    
      
        M
        (
        n
        )
      
    
    {\\displaystyle M(n)}
  
 indicates the time needed for multiplying two polynomials of degree at most 
  
    
      
        n
      
    
    {\\displaystyle n}
  
.


== Special functions ==
Many of the methods in this section are given in Borwein & Borwein.


=== Elementary functions ===
The elementary functions are constructed by composing arithmetic operations, the exponential function (
  
    
      
        exp
      
    
    {\\displaystyle \\exp }
  
), the natural logarithm (
  
    
      
        log
      
    
    {\\displaystyle \\log }
  
), trigonometric functions (
  
    
      
        sin
        ,
        cos
      
    
    {\\displaystyle \\sin ,\\cos }
  
), and their inverses. The complexity of an elementary function is equivalent to that of its inverse, since all elementary functions are analytic and hence invertible by means of Newton's method. In particular, if either 
  
    
      
        exp
      
    
    {\\displaystyle \\exp }
  
 or 
  
    
      
        log
      
    
    {\\displaystyle \\log }
  
 in the complex domain can be computed with some complexity, then that complexity is attainable for all other elementary functions.
Below, the size 
  
    
      
        n
      
    
    {\\displaystyle n}
  
 refers to the number of digits of precision at which the function is to be evaluated.

It is not known whether 
  
    
      
        O
        (
        M
        (
        n
        )
        log
        ⁡
        n
        )
      
    
    {\\displaystyle O(M(n)\\log n)}
  
 is the optimal complexity for elementary functions. The best known lower bound is the trivial bound 

  
    
      
        Ω
      
    
    {\\displaystyle \\Omega }
  

  
    
      
        (
        M
        (
        n
        )
        )
      
    
    {\\displaystyle (M(n))}
  
.


=== Non-elementary functions ===


=== Mathematical constants ===
This table gives the complexity of computing approximations to the given constants to 
  
    
      
        n
      
    
    {\\displaystyle n}
  
 correct digits.


== Number theory ==
Algorithms for number theoretical calculations are studied in computational number theory.


== Matrix algebra ==

The following complexity figures assume that arithmetic with individual elements has complexity O(1), as is the case with fixed-precision floating-point arithmetic or operations on a finite field.

In 2005, Henry Cohn, Robert Kleinberg, Balázs Szegedy, and Chris Umans showed that either of two different conjectures would imply that the exponent of matrix multiplication is 2.


== Transforms ==
Algorithms for computing transforms of functions (particularly integral transforms) are widely used in all areas of mathematics, particularly analysis and signal processing.


== Notes ==


== References ==


== Further reading ==""",
    tier=10,
    domain="deep_learning",
    source="Wikipedia, 'Computational complexity of mathematical operations'",
    source_url="https://en.wikipedia.org/wiki/Computational_complexity_of_mathematical_operations",
))

register_atom(Atom(
    atom_type="methodology",
    name="successor_design",
    content="""Neural architecture search (NAS) is a technique for automating the design of artificial neural networks (ANN), a widely used model in the field of machine learning. NAS has been used to design networks that are on par with or outperform hand-designed architectures. Methods for NAS can be categorized according to the search space, search strategy and performance estimation strategy used:

The search space defines the type(s) of ANN that can be designed and optimized.
The search strategy defines the approach used to explore the search space.
The performance estimation strategy evaluates the performance of a possible ANN from its design (without constructing and training it).
NAS is closely related to hyperparameter optimization and meta-learning and is a subfield of automated machine learning (AutoML).


== Reinforcement learning ==
Reinforcement learning (RL) can underpin a NAS search strategy. Barret Zoph and Quoc Viet Le applied NAS with RL targeting the CIFAR-10 dataset and achieved a network architecture that rivals the best manually-designed architecture for accuracy, with an error rate of 3.65, 0.09 percent better and 1.05x faster than a related hand-designed model. On the Penn Treebank dataset, that model composed a recurrent cell that outperforms LSTM, reaching a test set perplexity of 62.4, or 3.6 perplexity better than the prior leading system. On the PTB character language modeling task it achieved bits per character of 1.214.
Learning a model architecture directly on a large dataset can be a lengthy process. NASNet addressed this issue by transferring a building block designed for a small dataset to a larger dataset. The design was constrained to use two types of convolutional cells to return feature maps that serve two main functions when convoluting an input feature map: normal cells that return maps of the same extent (height and width) and reduction cells in which the returned feature map height and width is reduced by a factor of two. For the reduction cell, the initial operation applied to the cell's inputs uses a stride of two (to reduce the height and width). The learned aspect of the design included elements such as which lower layer(s) each higher layer took as input, the transformations applied at that layer and to merge multiple outputs at each layer. In the studied example, the best convolutional layer (or "cell") was designed for the CIFAR-10 dataset and then applied to the ImageNet dataset by stacking copies of this cell, each with its own parameters. The approach yielded accuracy of 82.7% top-1 and 96.2% top-5. This exceeded the best human-invented architectures at a cost of 9 billion fewer FLOPS—a reduction of 28%. The system continued to exceed the manually-designed alternative at varying computation levels. The image features learned from image classification can be transferred to other computer vision problems. E.g., for object detection, the learned cells integrated with the Faster-RCNN framework improved performance by 4.0% on the COCO dataset.
In the so-called Efficient Neural Architecture Search (ENAS), a controller discovers architectures by learning to search for an optimal subgraph within a large graph. The controller is trained with policy gradient to select a subgraph that maximizes the validation set's expected reward. The model corresponding to the subgraph is trained to minimize a canonical cross entropy loss. Multiple child models share parameters, ENAS requires fewer GPU-hours than other approaches and 1000-fold less than "standard" NAS. On CIFAR-10, the ENAS design achieved a test error of 2.89%, comparable to NASNet. On Penn Treebank, the ENAS design reached test perplexity of 55.8.


== Evolution ==
An alternative approach to NAS is based on evolutionary algorithms, which has been employed by several groups. An Evolutionary Algorithm for Neural Architecture Search generally performs the following procedure. First a pool consisting of different candidate architectures along with their validation scores (fitness) is initialised. At each step the architectures in the candidate pool are mutated (e.g.: 3x3 convolution instead of a 5x5 convolution). Next the new architectures are trained from scratch for a few epochs and their validation scores are obtained. This is followed by replacing the lowest scoring architectures in the candidate pool with the better, newer architectures. This procedure is repeated multiple times and thus the candidate pool is refined over time. Mutations in the context of evolving ANNs are operations such as adding or removing a layer, which include changing the type of a layer (e.g., from convolution to pooling), changing the hyperparameters of a layer, or changing the training hyperparameters. On CIFAR-10 and ImageNet, evolution and RL performed comparably, while both slightly outperformed random search.


== Bayesian optimization ==
Bayesian Optimization (BO), which has proven to be an efficient method for hyperparameter optimization, can also be applied to NAS. In this context, the objective function maps an architecture to its validation error after being trained for a number of epochs. At each iteration, BO uses a surrogate to model this objective function based on previously obtained architectures and their validation errors. One then chooses the next architecture to evaluate by maximizing an acquisition function, such as expected improvement, which provides a balance between exploration and exploitation. Acquisition function maximization and objective function evaluation are often computationally expensive for NAS, and make the application of BO challenging in this context. Recently, BANANAS has achieved promising results in this direction by introducing a high-performing instantiation of BO coupled to a neural predictor.


== Hill-climbing ==
Another group used a hill climbing procedure that applies network morphisms, followed by short cosine-annealing optimization runs. The approach yielded competitive results, requiring resources on the same order of magnitude as training a single network. E.g., on CIFAR-10, the method designed and trained a network with an error rate below 5% in 12 hours on a single GPU.


== Multi-objective search ==
While most approaches solely focus on finding architecture with maximal predictive performance, for most practical applications other objectives are relevant, such as memory consumption, model size or inference time (i.e., the time required to obtain a prediction). Because of that, researchers created a multi-objective search.
LEMONADE is an evolutionary algorithm that adopted Lamarckism to efficiently optimize multiple objectives. In every generation, child networks are generated to improve the Pareto frontier with respect to the current population of ANNs.
Neural Architect is claimed to be a resource-aware multi-objective RL-based NAS with network embedding and performance prediction. Network embedding encodes an existing network to a trainable embedding vector. Based on the embedding, a controller network generates transformations of the target network. A multi-objective reward function considers network accuracy, computational resource and training time. The reward is predicted by multiple performance simulation networks that are pre-trained or co-trained with the controller network. The controller network is trained via policy gradient. Following a modification, the resulting candidate network is evaluated by both an accuracy network and a training time network. The results are combined by a reward engine that passes its output back to the controller network.


== One-shot models ==
RL or evolution-based NAS require thousands of GPU-days of searching/training to achieve state-of-the-art computer vision results as described in the NASNet, mNASNet and MobileNetV3 papers.
To reduce computational cost, many recent NAS methods rely on the weight-sharing idea.""",
    tier=10,
    domain="deep_learning",
    source="Wikipedia, 'Neural architecture search'",
    source_url="https://en.wikipedia.org/wiki/Neural_architecture_search",
))

register_atom(Atom(
    atom_type="principle",
    name="lagrange_multiplier",
    content="""In mathematical optimization, the method of Lagrange multipliers is a strategy for finding the local maxima and minima of a function subject to equation constraints (i.e., subject to the condition that one or more equations have to be satisfied exactly by the chosen values of the variables). It is named after the mathematician Joseph-Louis Lagrange.


== Summary and rationale ==
The basic idea is to convert a constrained problem into a form such that the derivative test of an unconstrained problem can still be applied. The relationship between the gradient of the function and gradients of the constraints rather naturally leads to a reformulation of the original problem, known as the Lagrangian function or Lagrangian. In the general case, the Lagrangian is defined as

  
    
      
        
          
            L
          
        
        (
        x
        ,
        λ
        )
        ≡
        f
        (
        x
        )
        +
        ⟨
        λ
        ,
        g
        (
        x
        )
        ⟩
      
    
    {\\displaystyle {\\mathcal {L}}(x,\\lambda )\\equiv f(x)+\\langle \\lambda ,g(x)\\rangle }
  

for functions 
  
    
      
        f
        ,
        g
      
    
    {\\displaystyle f,g}
  
; the notation 
  
    
      
        ⟨
        ⋅
        ,
        ⋅
        ⟩
      
    
    {\\displaystyle \\langle \\cdot ,\\cdot \\rangle }
  
 denotes an inner product. The value 
  
    
      
        λ
      
    
    {\\displaystyle \\lambda }
  
 is called the Lagrange multiplier.
In simple cases, where the inner product is defined as the dot product, the Lagrangian is

  
    
      
        
          
            L
          
        
        (
        x
        ,
        λ
        )
        ≡
        f
        (
        x
        )
        +
        λ
        ⋅
        g
        (
        x
        )
      
    
    {\\displaystyle {\\mathcal {L}}(x,\\lambda )\\equiv f(x)+\\lambda \\cdot g(x)}
  

The method can be summarized as follows: in order to find the maximum or minimum of a function 
  
    
      
        f
      
    
    {\\displaystyle f}
  
 subject to the equality constraint 
  
    
      
        g
        (
        x
        )
        =
        0
      
    
    {\\displaystyle g(x)=0}
  
, find the stationary points of 
  
    
      
        
          
            L
          
        
      
    
    {\\displaystyle {\\mathcal {L}}}
  
 considered as a function of 
  
    
      
        x
      
    
    {\\displaystyle x}
  
 and the Lagrange multiplier 
  
    
      
        λ
         
      
    
    {\\displaystyle \\lambda ~}
  
. This means that all partial derivatives should be zero, including the partial derivative with respect to 
  
    
      
        λ
         
      
    
    {\\displaystyle \\lambda ~}
  
.

or equivalently

The solution corresponding to the original constrained optimization is always a saddle point of the Lagrangian function, which can be identified among the stationary points from the definiteness of the bordered Hessian matrix.
The great advantage of this method is that it allows the optimization to be solved without explicit parameterization in terms of the constraints. As a result, the method of Lagrange multipliers is widely used to solve challenging constrained optimization problems. Further, the method of Lagrange multipliers is generalized by the Karush–Kuhn–Tucker conditions, which can also take into account inequality constraints of the form 
  
    
      
        h
        (
        
          x
        
        )
        ≤
        c
      
    
    {\\displaystyle h(\\mathbf {x} )\\leq c}
  
 for a given constant 
  
    
      
        c
      
    
    {\\displaystyle c}
  
.


== Statement ==
The following is known as the Lagrange multiplier theorem.
Let 
  
    
      
        f
        :
        
          
            R
          
          
            n
          
        
        →
        
          R
        
      
    
    {\\displaystyle f\\colon \\mathbb {R} ^{n}\\to \\mathbb {R} }
  
 be the objective function and let 
  
    
      
        g
        :
        
          
            R
          
          
            n
          
        
        →
        
          
            R
          
          
            c
          
        
      
    
    {\\displaystyle g\\colon \\mathbb {R} ^{n}\\to \\mathbb {R} ^{c}}
  
 be the constraints function, both belonging to 
  
    
      
        
          C
          
            1
          
        
      
    
    {\\displaystyle C^{1}}
  
 (that is, having continuous first derivatives). Consider the following constrained optimization problem:

  
    
      
        
          
            
              
              
                
                  maximize 
                
                f
                (
                x
                )
              
            
            
              
              
                
                  subject to: 
                
                g
                (
                x
                )
                =
                0
              
            
          
        
      
    
    {\\displaystyle {\\begin{aligned}&{\\text{maximize }}f(x)\\\\&{\\text{subject to: }}g(x)=0\\end{aligned}}}
  

Let 
  
    
      
        
          x
          
            ⋆
          
        
      
    
    {\\displaystyle x_{\\star }}
  
 be an optimal solution to the above optimization problem such that, for the matrix of partial derivatives 
  
    
      
        
          
            [
          
        
        D
        ⁡
        g
        (
        
          x
          
            ⋆
          
        
        )
        
          
            
              ]
            
          
          
            j
            ,
            k
          
        
        =
        
          
            
               
              ∂
              
                g
                
                  j
                
              
               
            
            
              ∂
              
                x
                
                  k
                
              
            
          
        
      
    
    {\\displaystyle {\\Bigl [}\\operatorname {D} g(x_{\\star }){\\Bigr ]}_{j,k}={\\frac {\\ \\partial g_{j}\\ }{\\partial x_{k}}}}
  
, 
  
    
      
        rank
        ⁡
        (
        D
        ⁡
        g
        (
        
          x
          
            ⋆
          
        
        )
        )
        =
        c
        ≤
        n
      
    
    {\\displaystyle \\operatorname {rank} (\\operatorname {D} g(x_{\\star }))=c\\leq n}
  
:
Then there exists a unique Lagrange multiplier 
  
    
      
        
          λ
          
            ⋆
          
        
        ∈
        
          
            R
          
          
            c
          
        
      
    
    {\\displaystyle \\lambda _{\\star }\\in \\mathbb {R} ^{c}}
  
 such that 
  
    
      
        D
        ⁡
        f
        (
        
          x
          
            ⋆
          
        
        )
        =
        
          λ
          
            ⋆
          
          
            
              T
            
          
        
        D
        ⁡
        g
        (
        
          x
          
            ⋆
          
        
        )
         
        .
      
    
    {\\displaystyle \\operatorname {D} f(x_{\\star })=\\lambda _{\\star }^{\\mathsf {T}}\\operatorname {D} g(x_{\\star })~.}
  
 (In this equation, 
  
    
      
        
          λ
          
            ⋆
          
        
      
    
    {\\displaystyle \\lambda _{\\star }}
  
 is a column vector, so its transpose 
  
    
      
        
          λ
          
            ⋆
          
          
            
              T
            
          
        
      
    
    {\\displaystyle \\lambda _{\\star }^{\\mathsf {T}}}
  
 is a row vector.""",
    tier=7,
    domain="optimisation",
    source="Wikipedia, 'Lagrange multiplier'",
    source_url="https://en.wikipedia.org/wiki/Lagrange_multiplier",
))

register_atom(Atom(
    atom_type="algorithm",
    name="sorting",
    content="""In computer science, a sorting algorithm is an algorithm that puts elements of a list into an order. The most frequently used orders are numerical order and lexicographical order, and either ascending order or descending order. Efficient sorting is important for optimizing the efficiency of other algorithms (such as search and merge algorithms) that require input data to be in sorted lists. Sorting is also often useful for canonicalizing data and for producing human-readable output.
Formally, the output of any sorting algorithm must satisfy two conditions:

The output is in monotonic order (each element is no smaller/larger than the previous element, according to the required order).
The output is a permutation (a reordering, yet retaining all of the original elements) of the input.
Although some algorithms are designed for sequential access, the highest-performing algorithms assume data is stored in a data structure which allows random access.


== History and concepts ==
From the beginning of computing, the sorting problem has attracted a great deal of research, perhaps due to the complexity of solving it efficiently despite its simple, familiar statement. Among the authors of early sorting algorithms around 1951 was Betty Holberton, who worked on ENIAC and UNIVAC. Bubble sort was analyzed as early as 1956. Asymptotically optimal algorithms have been known since the mid-20th century –  new algorithms are still being invented, with the widely used Timsort dating to 2002, and the library sort being first published in 2006.
Comparison sorting algorithms have a fundamental requirement of 
  
    
      
        n
        log
        ⁡
        
          n
        
        −
        1.4427
        n
        +
        O
        (
        log
        ⁡
        
          n
        
        )
      
    
    {\\displaystyle n\\log {n}-1.4427n+O(\\log {n})}
  
 comparisons. Algorithms not based on comparisons, such as counting sort, can have better performance.
Sorting algorithms are prevalent in introductory computer science classes, where the abundance of algorithms for the problem provides a gentle introduction to a variety of core algorithm concepts, such as big O notation, divide-and-conquer algorithms, data structures such as heaps and binary trees, randomized algorithms, best, worst and average case analysis, time–space tradeoffs, and upper and lower bounds.
Sorting small arrays optimally (in the fewest comparisons and swaps) or fast (i.e. taking into account machine-specific details) is still an open research problem, with solutions only known for very small arrays (fewer than 20 elements). Similarly optimal (by various definitions) sorting on a parallel machine is an open research topic.


== Classification ==
Sorting algorithms can be classified by:

Computational complexity
Best, worst and average case behavior in terms of the size of the list. For typical serial sorting algorithms, good behavior is O(n log n), with parallel sort in O(log2 n), and bad behavior is O(n2). Ideal behavior for a serial sort is O(n), but this is not possible in the average case. Optimal parallel sorting is O(log n).
Swaps for "in-place" algorithms.
Memory usage (and use of other computer resources). In particular, some sorting algorithms are "in-place". Strictly, an in-place sort needs only O(1) memory beyond the items being sorted; sometimes O(log n) additional memory is considered "in-place".
Recursion: Some algorithms are either typically recursive or typically non-recursive, while others may typically be both (e.g., merge sort).
Stability: stable sorting algorithms maintain the relative order of records with equal keys (i.e., values).
Whether or not they are a comparison sort. A comparison sort examines the data only by comparing two elements with a comparison operator.
General method: insertion, exchange, selection, merging, etc. Exchange sorts include bubble sort and quicksort. Selection sorts include cycle sort and heapsort.
Whether the algorithm is serial or parallel. The remainder of this discussion almost exclusively concentrates on serial algorithms and assumes serial operation.
Adaptability: Whether or not the presortedness of the input affects the running time.  Algorithms that take this into account are known to be adaptive.
Online: An algorithm such as Insertion Sort that is online can sort a constant stream of input.


=== Stability ===

Stable sorting algorithms sort equal elements in the same order that they appear in the input. For example, in the card sorting example to the right, the cards are being sorted by their rank, and their suit is being ignored. This allows the possibility of multiple different correctly sorted versions of the original list. Stable sorting algorithms choose one of these, according to the following rule: if two items compare as equal (like the two 5 cards), then their relative order will be preserved, i.e. if one comes before the other in the input, it will come before the other in the output.
Stability is important to preserve order over multiple sorts on the same data set. For example, say that student records consisting of name and class section are sorted dynamically, first by name, then by class section. If a stable sorting algorithm is used in both cases, the sort-by-class-section operation will not change the name order; with an unstable sort, it could be that sorting by section shuffles the name order, resulting in a nonalphabetical list of students.
More formally, the data being sorted can be represented as a record or tuple of values, and the part of the data that is used for sorting is called the key. In the card example, cards are represented as a record (rank, suit), and the key is the rank. A sorting algorithm is stable if whenever there are two records R and S with the same key, and R appears before S in the original list, then R will always appear before S in the sorted list.
When equal elements are indistinguishable, such as with integers, or more generally, any data where the entire element is the key, stability is not an issue. Stability is also not an issue if all keys are different.
Unstable sorting algorithms can be specially implemented to be stable. One way of doing this is to artificially extend the key comparison so that comparisons between two objects with otherwise equal keys are decided using the order of the entries in the original input list as a tie-breaker. Remembering this order, however, may require additional time and space.
One application for stable sorting algorithms is sorting a list using a primary and secondary key. For example, suppose we wish to sort a hand of cards such that the suits are in the order clubs (♣), diamonds (♦), hearts (♥), spades (♠), and within each suit, the cards are sorted by rank. This can be done by first sorting the cards by rank (using any sort), and then doing a stable sort by suit:

Within each suit, the stable sort preserves the ordering by rank that was already done. This idea can be extended to any number of keys and is utilised by radix sort. The same effect can be achieved with an unstable sort by using a lexicographic key comparison, which, e.g., compares first by suit, and then compares by rank if the suits are the same.


== Comparison of algorithms ==
This analysis assumes that the length of each key is constant and that all comparisons, swaps and other operations can proceed in constant time.
Legend:

n is the number of records to be sorted.
Comparison column has the following ranking classifications: "Best", "Average" and "Worst" if the time complexity is given for each case.
"Memory" denotes the amount of additional storage required by the algorithm.
The run times and the memory requirements listed are inside big O notation, hence the base of the logarithms does not matter.
The notation log2 n means (log n)2.


=== Comparison sorts ===
Below is a table of comparison sorts.""",
    tier=0,
    domain="arithmetic",
    source="Wikipedia, 'Sorting algorithm'",
    source_url="https://en.wikipedia.org/wiki/Sorting_algorithm",
))

register_atom(Atom(
    atom_type="algorithm",
    name="digit_root",
    content="""The digital root (also repeated digital sum) of a natural number in a given radix is the (single digit) value obtained by an iterative process of summing digits, on each iteration using the result from the previous iteration to compute a digit sum. The process continues until a single-digit number is reached. For example, in base 10, the digital root of the number 12345 is 6 because the sum of the digits in the number is 1 + 2 + 3 + 4 + 5 = 15, then the addition process is repeated again for the resulting number 15, so that the sum of 1 + 5 equals 6, which is the digital root of that number. In base 10, this is equivalent to taking the remainder upon division by 9 (except when the digital root is 9, where the remainder upon division by 9 will be 0), which allows it to be used as a divisibility rule.


== Formal definition ==
Let 
  
    
      
        n
      
    
    {\\displaystyle n}
  
 be a natural number. For base 
  
    
      
        b
        >
        1
      
    
    {\\displaystyle b>1}
  
, we define the digit sum 
  
    
      
        
          F
          
            b
          
        
        :
        
          N
        
        →
        
          N
        
      
    
    {\\displaystyle F_{b}:\\mathbb {N} \\rightarrow \\mathbb {N} }
  
 to be the following:

  
    
      
        
          F
          
            b
          
        
        (
        n
        )
        =
        
          ∑
          
            i
            =
            0
          
          
            k
            −
            1
          
        
        
          d
          
            i
          
        
      
    
    {\\displaystyle F_{b}(n)=\\sum _{i=0}^{k-1}d_{i}}
  

where 
  
    
      
        k
        =
        ⌊
        
          log
          
            b
          
        
        ⁡
        
          n
        
        ⌋
        +
        1
      
    
    {\\displaystyle k=\\lfloor \\log _{b}{n}\\rfloor +1}
  
 is the number of digits in the number in base 
  
    
      
        b
      
    
    {\\displaystyle b}
  
, and

  
    
      
        
          d
          
            i
          
        
        =
        
          
            
              n
              
                mod
                
                  
                    b
                    
                      i
                      +
                      1
                    
                  
                
              
              −
              n
              
                
                  mod
                  
                    b
                  
                
                
                  i
                
              
            
            
              b
              
                i
              
            
          
        
      
    
    {\\displaystyle d_{i}={\\frac {n{\\bmod {b^{i+1}}}-n{\\bmod {b}}^{i}}{b^{i}}}}
  

is the value of each digit of the number. A natural number 
  
    
      
        n
      
    
    {\\displaystyle n}
  
 is a digital root if it is a fixed point for 
  
    
      
        
          F
          
            b
          
        
      
    
    {\\displaystyle F_{b}}
  
, which occurs if 
  
    
      
        
          F
          
            b
          
        
        (
        n
        )
        =
        n
      
    
    {\\displaystyle F_{b}(n)=n}
  
. 
All natural numbers 
  
    
      
        n
      
    
    {\\displaystyle n}
  
 are preperiodic points for 
  
    
      
        
          F
          
            b
          
        
      
    
    {\\displaystyle F_{b}}
  
, regardless of the base. This is because if 
  
    
      
        n
        ≥
        b
      
    
    {\\displaystyle n\\geq b}
  
, then

  
    
      
        n
        =
        
          ∑
          
            i
            =
            0
          
          
            k
            −
            1
          
        
        
          d
          
            i
          
        
        
          b
          
            i
          
        
      
    
    {\\displaystyle n=\\sum _{i=0}^{k-1}d_{i}b^{i}}
  

and therefore

  
    
      
        
          F
          
            b
          
        
        (
        n
        )
        =
        
          ∑
          
            i
            =
            0
          
          
            k
            −
            1
          
        
        
          d
          
            i
          
        
        <
        
          ∑
          
            i
            =
            0
          
          
            k
            −
            1
          
        
        
          d
          
            i
          
        
        
          b
          
            i
          
        
        =
        n
      
    
    {\\displaystyle F_{b}(n)=\\sum _{i=0}^{k-1}d_{i}<\\sum _{i=0}^{k-1}d_{i}b^{i}=n}
  

because 
  
    
      
        b
        >
        1
      
    
    {\\displaystyle b>1}
  
.
If 
  
    
      
        n
        <
        b
      
    
    {\\displaystyle n<b}
  
, then trivially 

  
    
      
        
          F
          
            b
          
        
        (
        n
        )
        =
        n
      
    
    {\\displaystyle F_{b}(n)=n}
  

Therefore, the only possible digital roots are the natural numbers 
  
    
      
        0
        ≤
        n
        <
        b
      
    
    {\\displaystyle 0\\leq n<b}
  
, and there are no cycles other than the fixed points of 
  
    
      
        0
        ≤
        n
        <
        b
      
    
    {\\displaystyle 0\\leq n<b}
  
.


=== Example ===
In base 12, 8 is the additive digital root of the base 10 number 3110, as for 
  
    
      
        n
        =
        3110
      
    
    {\\displaystyle n=3110}
  

  
    
      
        
          d
          
            0
          
        
        =
        
          
            
              3110
              
                mod
                
                  
                    12
                    
                      0
                      +
                      1
                    
                  
                
              
              −
              3110
              
                mod
                
                  1
                
              
              
                2
                
                  0
                
              
            
            
              12
              
                0
              
            
          
        
        =
        
          
            
              3110
              
                mod
                
                  12
                
              
              −
              3110
              
                mod
                
                  1
                
              
            
            1
          
        
        =
        
          
            
              2
              −
              0
            
            1
          
        
        =
        
          
            2
            1
          
        
        =
        2
      
    
    {\\displaystyle d_{0}={\\frac {3110{\\bmod {12^{0+1}}}-3110{\\bmod {1}}2^{0}}{12^{0}}}={\\frac {3110{\\bmod {12}}-3110{\\bmod {1}}}{1}}={\\frac {2-0}{1}}={\\frac {2}{1}}=2}
  

  
    
      
        
          d
          
            1
          
        
        =
        
          
            
              3110
              
                mod
                
                  
                    12
                    
                      1
                      +
                      1
                    
                  
                
              
              −
              3110
              
                mod
                
                  1
                
              
              
        """,
    tier=0,
    domain="arithmetic",
    source="Wikipedia, 'Digital root'",
    source_url="https://en.wikipedia.org/wiki/Digital_root",
))

register_atom(Atom(
    atom_type="algorithm",
    name="caesar",
    content="""A Caesar cipher is one of the simplest and most widely known encryption techniques used in cryptography. It is a type of substitution cipher in which each letter in the plaintext is replaced by a letter some fixed number of positions along the alphabet. For example, with a left shift of 3, D would be replaced by A, E would become B, and so on. The method is named after Julius Caesar, who used it in his private correspondence.
The encryption step performed by a Caesar cipher is often incorporated as part of more complex schemes, such as the Vigenère cipher, and still has modern application in the ROT13 system. As with all single-alphabet substitution ciphers, the Caesar cipher is easily broken and in modern practice offers essentially no communications security.


== Example ==

The transformation can be represented by aligning two alphabets; the cipher is the plain alphabet shifted left or right by a certain number of positions. For instance, here is a Caesar cipher using a left shift of 3 places, equivalent to a right shift of 23 (the shift parameter is used as the key):

When encrypting, a person looks up each letter of the message in the "plain" line and writes down the corresponding letter in the "cipher" line.

Plaintext:  THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG
Ciphertext: QEB NRFZH YOLTK CLU GRJMP LSBO QEB IXWV ALD

Deciphering is done in reverse, with a right shift of 3.
The encryption can also be represented using modular arithmetic by first transforming the letters into numbers, according to the scheme, A → 0, B → 1, ..., Z → 25. Encryption of a letter x by a shift n can be described mathematically as:

  
    
      
        
          E
          
            n
          
        
        (
        x
        )
        =
        (
        x
        +
        n
        )
        
        mod
        
        
        26.
      
    
    {\\displaystyle E_{n}(x)=(x+n)\\mod {26}.}
  

Decryption is performed similarly:

  
    
      
        
          D
          
            n
          
        
        (
        x
        )
        =
        (
        x
        −
        n
        )
        
        mod
        
        
        26.
      
    
    {\\displaystyle D_{n}(x)=(x-n)\\mod {26}.}
  

(Here, "mod" refers to the modulo operation. The value x is in the range 0 to 25, but if x + n or x − n are not in this range then 26 should be added or subtracted.)
The replacement remains the same throughout the message, so the cipher is classed as a type of monoalphabetic substitution, as opposed to polyalphabetic substitution.


== History and usage ==

The Caesar cipher is named for Julius Caesar, who, according to the Roman historian Suetonius, used it with a shift of three (A becoming D when encrypting, and vice versa when decrypting) to protect messages of military significance. While Caesar's was the first recorded use of this scheme, other substitution ciphers are known to have existed earlier. Suetonius writes that his nephew, Augustus, used the cipher with a right shift of one, but it did not wrap around to the beginning of the Latin alphabet, instead replacing Z with AA. Evidence exists that Caesar also used more complicated systems. The grammarian Aulus Gellius refers to a (now lost) treatise on his ciphers:"There is even a rather ingeniously written treatise by the grammarian Probus concerning the secret meaning of letters in the composition of Caesar's epistles."
It is unknown how effective the Caesar cipher was at the time: there is no record of contemporary techniques for the solution of simple substitution ciphers. The earliest surviving records date to the 9th-century works of Al-Kindi in the Arab world with the discovery of frequency analysis.
A piece of text encrypted in a Hebrew version of the Caesar cipher (not to be confused with Atbash) is sometimes found on the back of Jewish mezuzah scrolls. When each letter is replaced with the letter before it in the Hebrew alphabet, the text reads "YHWH, our God, YHWH", a quotation from the scroll.
The Vigenère cipher uses a Caesar cipher with a different shift at each position in the text; the value of the shift is defined using a repeating keyword. Repeating keywords (e.g., "Complete Victory" used by the Confederacy during the American Civil War) introduce a cyclic pattern that might be detected with statistically advanced frequency analysis. (See e.g. Coincidence counting.) If the keyword is as long as the message, is chosen at random, never becomes known to anyone else, and is never reused, it is a one-time pad cipher, impossible to break cryptographically. However, the problems involved in distributing such a key make the one-time pad difficult to use in practice.
In the 19th century, the personal advertisements section in newspapers would sometimes be used to exchange messages encrypted using simple cipher schemes. David Kahn (1967) describes instances of lovers engaging in secret communications enciphered using the Caesar cipher in The Times. As late as 1915 during World War I, the Caesar cipher was used by the Russian army as a replacement for more complicated ciphers which had proven difficult for their troops to master; German and Austrian cryptanalysts had little difficulty in decrypting their messages.

In April 2006, fugitive Mafia boss Bernardo Provenzano was captured in Sicily partly because some of his messages, clumsily written in a variation of the Caesar cipher, were broken. Provenzano's cipher used numbers, so that "A" would be written as "4", "B" as "5", and so on.
In 2011, British Airways employee Rajib Karim was convicted of "terrorism offences" after using a Caesar cipher to discuss with Bangladeshi jihadi activists plots to bomb the airline's planes or disrupt its IT systems. Although the parties had access to far better encryption techniques (Karim himself used PGP for data storage), they chose to use their own scheme implemented in Microsoft Excel, rejecting a more sophisticated code program called Mujahedeen Secrets "because 'kaffirs', or non-believers, know about it, so it must be less secure".
Caesar ciphers can be found today in children's toys such as secret decoder rings. A Caesar shift of thirteen is also performed in the ROT13 cipher, a simple method of obfuscating text widely found on Usenet and used to obscure text (such as joke punchlines and story spoilers), but not seriously used as a method of encryption.


== Breaking the cipher ==

The Caesar cipher can be easily broken even in a ciphertext-only scenario. Since there are only a limited number of possible shifts (25 in English), an attacker can mount a brute force attack by deciphering the message, or part of it, using each possible shift. The correct decryption will be the one which makes sense in the language of the plaintext. An example is shown on the right for the ciphertext "exxegoexsrgi"; the candidate plaintext for shift four, "attackatonce", is the only one which makes sense as English text. Another type of brute force attack is to write out the alphabet beneath each letter of the ciphertext, starting at that letter. Again the correct decryption is the one which makes sense as English text. This technique is sometimes known as "completing the plain component".

Another approach is to match up the frequency distribution of the letters. By graphing the frequencies of letters in the ciphertext, and by knowing the expected distribution of those letters in the original language of the plaintext, a human can easily spot the value of the shift by looking at the displacement of particular features of the graph. This is known as frequency analysis. For example, in the English language the plaintext frequencies of the letters E, T, (usually most frequent), and Q, Z (typically least frequent) are particularly distinctive. Computers can automate this process by assessing the similarity between the observed frequency distribution and the expected distribution.""",
    tier=1,
    domain="cryptography",
    source="Wikipedia, 'Caesar cipher'",
    source_url="https://en.wikipedia.org/wiki/Caesar_cipher",
))

register_atom(Atom(
    atom_type="algorithm",
    name="run_length",
    content="""Run-length encoding (RLE) is a form of lossless data compression in which runs of data (consecutive occurrences of the same data value) are stored as a single occurrence of that data value and a count of its consecutive occurrences, rather than as the original run. For example, a sequence of "green green green green green" in an image built up from colored dots could be shortened to "green x 5".
Run-length encoding is most efficient on data that contains many such runs, for example, simple graphic images such as icons, line drawings, games, and animations. For files that do not have many runs, encoding them with RLE could increase the file size.
RLE may also refer to particular image formats that use the encoding. RLE is an early graphics file format supported by CompuServe for compressing black and white images, that was widely supplanted by their later Graphics Interchange Format (GIF). It is also the name of a little-used image format in Windows 3.x that is saved with the file extension rle, consisting of a run-length encoded bitmap; it was used as the format for the Windows 3.x startup screen.


== History and applications ==
Run-length encoding (RLE) schemes were employed in the transmission of analog television signals as far back as 1967. In 1983, run-length encoding was patented by Hitachi. RLE is particularly well suited to palette-based bitmap images (which use relatively few colors) such as computer icons, and was a popular image compression method on early online services such as CompuServe before the advent of more sophisticated formats such as GIF.  It does not work well on continuous-tone images (which use very many colors) such as photographs, although JPEG uses it on the coefficients that remain after transforming and quantizing image blocks.
Common formats for run-length encoded data include Truevision TGA, PackBits (by Apple, used in MacPaint), PCX and ILBM.  The International Telecommunication Union also describes a standard to encode run-length color for fax machines, known as T.45.  That fax color coding standard, which along with other techniques is incorporated into Modified Huffman coding, is relatively efficient because most faxed documents are primarily white space, with occasional interruptions of black.


== Algorithm ==
RLE has a space complexity of ⁠
  
    
      
        O
        (
        n
        )
      
    
    {\\displaystyle O(n)}
  
⁠, where n is the size of the input data.


=== Encoding algorithm ===
Run-length encoding compresses data by reducing the physical size of a repeating string of characters. This process involves converting the input data into a compressed format by identifying and counting consecutive occurrences of each character. The steps are as follows:

Traverse the input data.
Count the number of consecutive repeating characters (run length).
Store the character and its run length.


==== Python implementation ====


=== Decoding algorithm ===
The decoding process involves reconstructing the original data from the encoded format by repeating characters according to their counts. The steps are as follows:

Traverse the encoded data.
For each count-character pair, repeat the character count times.
Append these characters to the result string.


==== Python implementation ====


== Example ==
Consider a screen containing plain black text on a solid white background.  There will be many long runs of white pixels in the blank space, and many short runs of black pixels within the text. A hypothetical scan line, with B representing a black pixel and W representing white, might read as follows:

 WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWBWWWWWWWWWWWWWW 
With a run-length encoding (RLE) data compression algorithm applied to the above hypothetical scan line, it can be rendered as follows:

 12W1B12W3B24W1B14W 
This can be interpreted as a sequence of twelve Ws, one B, twelve Ws, three Bs, etc., and represents the original 67 characters in only 18.  While the actual format used for the storage of images is generally binary rather than ASCII characters like this, the principle remains the same.  Even binary data files can be compressed with this method; file format specifications often dictate repeated bytes in files as padding space.  However, newer compression methods such as DEFLATE often use LZ77-based algorithms, a generalization of run-length encoding that can take advantage of runs of strings of characters (such as BWWBWWBWWBWW).
Run-length encoding can be expressed in multiple ways to accommodate data properties as well as additional compression algorithms.  For instance, one popular method encodes run lengths for runs of two or more characters only, using an "escape" symbol to identify runs, or using the character itself as the escape, so that any time a character appears twice it denotes a run.  On the previous example, this would give the following:

WW12BWW12BB3WW24BWW14
This would be interpreted as a run of twelve Ws, a B, a run of twelve Ws, a run of three Bs, etc.  In data where runs are less frequent, this can significantly improve the compression rate.
One other matter is the application of additional compression algorithms.  Even with the runs extracted, the frequencies of different characters may be large, allowing for further compression; however, if the run lengths are written in the file in the locations where the runs occurred, the presence of these numbers interrupts the normal flow and makes it harder to compress.  To overcome this, some run-length encoders separate the data and escape symbols from the run lengths, so that the two can be handled independently.  For the example data, this would result in two outputs, the string "WWBWWBBWWBWW" and the numbers (12,12,3,24,14).


== Variants ==
Sequential RLE: This method processes data one line at a time, scanning from left to right. It is commonly employed in image compression. Other variations of this technique include scanning the data vertically, diagonally, or in blocks.
Lossy RLE: In this variation, some bits are intentionally discarded during compression (often by setting one or two significant bits of each pixel to 0). This leads to higher compression rates while minimally impacting the visual quality of the image.
Adaptive RLE: Uses different encoding schemes depending on the length of runs to optimize compression ratios. For example, short runs might use a different encoding format than long runs.


== See also ==
Kolakoski sequence
Look-and-say sequence
Comparison of graphics file formats
Golomb coding
Burrows–Wheeler transform
Recursive indexing
Run-length limited
Bitmap index
Forsyth–Edwards Notation, which uses run-length-encoding for empty spaces in chess positions.
DEFLATE
Convolution
Huffman coding
Arithmetic coding


== References ==


== External links ==
Run-length encoding implemented in different programming languages (on Rosetta Code)
Single Header Run-Length Encoding Library smallest possible implementation (about 20 SLoC) in ANSI C. FOSS, compatible with Truevision TGA, supports 8, 16, 24 and 32 bit elements too.""",
    tier=1,
    domain="compression",
    source="Wikipedia, 'Run-length encoding'",
    source_url="https://en.wikipedia.org/wiki/Run-length_encoding",
))

register_atom(Atom(
    atom_type="theorem",
    name="derivative",
    content="""In mathematics, the derivative is a fundamental tool that quantifies the sensitivity to change of a function's output with respect to its input. The derivative of a function of a single variable at a chosen input value, when it exists, is the slope of the tangent line to the graph of the function at that point. The tangent line is the best linear approximation of the function near that input value. The derivative is often described as the instantaneous rate of change, the ratio of the instantaneous change in the dependent variable to that of the independent variable. The process of finding a derivative is called differentiation.
There are multiple different notations for differentiation. Leibniz notation, named after Gottfried Wilhelm Leibniz, is represented as the ratio of two differentials, whereas prime notation is written by adding a prime mark. Higher order notations represent repeated differentiation, and they are usually denoted in Leibniz notation by adding superscripts to the differentials, and in prime notation by adding additional prime marks. Higher order derivatives are used in physics; for example, the first derivative  with respect to time of the position of a moving object is its velocity, and the second derivative is its acceleration.
Derivatives can be generalized to functions of several real variables. In this case, the derivative is reinterpreted as a linear transformation whose graph is (after an appropriate translation) the best linear approximation to the graph of the original function. The Jacobian matrix is the matrix that represents this linear transformation with respect to the basis given by the choice of independent and dependent variables.  It can be calculated in terms of the partial derivatives with respect to the independent variables.  For a real-valued function of several variables, the Jacobian matrix reduces to the gradient vector.


== Definition ==


=== As a limit ===
A function of a real variable 
  
    
      
        f
        (
        x
        )
      
    
    {\\displaystyle f(x)}
  
 is differentiable at a point 
  
    
      
        a
      
    
    {\\displaystyle a}
  
 of its domain, if its domain contains an open interval containing ⁠
  
    
      
        a
      
    
    {\\displaystyle a}
  
⁠, and the limit

  
    
      
        L
        =
        
          lim
          
            h
            →
            0
          
        
        
          
            
              f
              (
              a
              +
              h
              )
              −
              f
              (
              a
              )
            
            h
          
        
      
    
    {\\displaystyle L=\\lim _{h\\to 0}{\\frac {f(a+h)-f(a)}{h}}}
  

exists.  This means that, for every positive real number ⁠
  
    
      
        ε
      
    
    {\\displaystyle \\varepsilon }
  
⁠, there exists a positive real number 
  
    
      
        δ
      
    
    {\\displaystyle \\delta }
  
 such that, for every 
  
    
      
        h
      
    
    {\\displaystyle h}
  
 such that 
  
    
      
        
          |
        
        h
        
          |
        
        <
        δ
      
    
    {\\displaystyle |h|<\\delta }
  
 and 
  
    
      
        h
        ≠
        0
      
    
    {\\displaystyle h\\neq 0}
  
 then 
  
    
      
        f
        (
        a
        +
        h
        )
      
    
    {\\displaystyle f(a+h)}
  
 is defined, and 

  
    
      
        
          |
          
            L
            −
            
              
                
                  f
                  (
                  a
                  +
                  h
                  )
                  −
                  f
                  (
                  a
                  )
                
                h
              
            
          
          |
        
        <
        ε
        ,
      
    
    {\\displaystyle \\left|L-{\\frac {f(a+h)-f(a)}{h}}\\right|<\\varepsilon ,}
  

where the vertical bars denote the absolute value. This is an example of the (ε, δ)-definition of limit.
If the function 
  
    
      
        f
      
    
    {\\displaystyle f}
  
 is differentiable at ⁠
  
    
      
        a
      
    
    {\\displaystyle a}
  
⁠, that is if the limit 
  
    
      
        L
      
    
    {\\displaystyle L}
  
 exists, then this limit is called the derivative of 
  
    
      
        f
      
    
    {\\displaystyle f}
  
 at ⁠
  
    
      
        a
      
    
    {\\displaystyle a}
  
⁠. Multiple notations for the derivative exist. The derivative of 
  
    
      
        f
      
    
    {\\displaystyle f}
  
 at 
  
    
      
        a
      
    
    {\\displaystyle a}
  
 can be denoted ⁠
  
    
      
        
          f
          ′
        
        (
        a
        )
      
    
    {\\displaystyle f'(a)}
  
⁠, read as "⁠
  
    
      
        f
      
    
    {\\displaystyle f}
  
⁠ prime of ⁠
  
    
      
        a
      
    
    {\\displaystyle a}
  
⁠"; or it can be denoted ⁠
  
    
      
        
          
            
              
                d
                f
              
              
                d
                x
              
            
          
          (
          a
          )
        
      
    
    {\\displaystyle \\textstyle {\\frac {df}{dx}}(a)}
  
⁠, read as "the derivative of 
  
    
      
        f
      
    
    {\\displaystyle f}
  
 with respect to 
  
    
      
        x
      
    
    {\\displaystyle x}
  
 at ⁠
  
    
      
        a
      
    
    {\\displaystyle a}
  
⁠" or "⁠
  
    
      
        d
        f
      
    
    {\\displaystyle df}
  
⁠ by (or over) 
  
    
      
        d
        x
      
    
    {\\displaystyle dx}
  
 at ⁠
  
    
      
        a
      
    
    {\\displaystyle a}
  
⁠". See § Notation below. If 
  
    
      
        f
      
    
    {\\displaystyle f}
  
 is a function that has a derivative at every point in its domain, then a function can be defined by mapping every point 
  
    
      
        x
      
    
    {\\displaystyle x}
  
 to the value of the derivative of 
  
    
      
        f
      
    
    {\\displaystyle f}
  
 at ⁠
  
    
      
        x
      
    
    {\\displaystyle x}
  
⁠. This function is written 
  
    
      
        
          f
          ′
        
      
    
    {\\displaystyle f'}
  
 and is called the derivative function or the derivative of ⁠
  
    
      
        f
      
    
    {\\displaystyle f}
  
⁠. The function 
  
    
      
        f
      
    
    {\\displaystyle f}
  
 sometimes has a derivative at most, but not all, points of its domain. The function whose value at 
  
    
      
        a
      
    
    {\\displaystyle a}
  
 equals 
  
    
      
        
          f
          ′
        
        (
        a
        )
      
    
    {\\displaystyle f'(a)}
  
 whenever 
  
    
      
        
          f
          ′
        
        (
        a
        )
      
    
    {\\displaystyle f'(a)}
  
 is defined and elsewhere is undefined is also called the derivative of ⁠
  
    
      
        f
      
    
    {\\displaystyle f}
  
⁠. It is still a function, but its domain may be smaller than the domain of ⁠
  
    
      
        f
      
    
    {\\displaystyle f}
  
⁠.
For example, let 
  
    
      
        f
      
    
    {\\displaystyle f}
  
 be the squaring function: ⁠
  
    
      
        f
        (
        x
        )
        =
        
          x
          
            2
          
        
      
    
    {\\displaystyle f(x)=x^{2}}
  
⁠.""",
    tier=2,
    domain="calculus",
    source="Wikipedia, 'Derivative'",
    source_url="https://en.wikipedia.org/wiki/Derivative",
))

register_atom(Atom(
    atom_type="algorithm",
    name="graph_reach",
    content="""In graph theory, reachability refers to the ability to get from one vertex to another within a graph. A vertex 
  
    
      
        s
      
    
    {\\displaystyle s}
  
 can reach a vertex 
  
    
      
        t
      
    
    {\\displaystyle t}
  
 (and 
  
    
      
        t
      
    
    {\\displaystyle t}
  
 is reachable from 
  
    
      
        s
      
    
    {\\displaystyle s}
  
) if there exists a sequence of adjacent vertices (i.e. a walk) which starts with 
  
    
      
        s
      
    
    {\\displaystyle s}
  
 and ends with 
  
    
      
        t
      
    
    {\\displaystyle t}
  
.
In an undirected graph, reachability between all pairs of vertices can be determined by identifying the connected components of the graph. Any pair of vertices in such a graph can reach each other if and only if they belong to the same connected component; therefore, in such a graph, reachability is symmetric (
  
    
      
        s
      
    
    {\\displaystyle s}
  
 reaches 
  
    
      
        t
      
    
    {\\displaystyle t}
  
 iff 
  
    
      
        t
      
    
    {\\displaystyle t}
  
 reaches 
  
    
      
        s
      
    
    {\\displaystyle s}
  
). The connected components of an undirected graph can be identified in linear time. The remainder of this article focuses on the more difficult problem of determining pairwise reachability in a directed graph (which, incidentally, need not be symmetric).


== Definition ==
For a directed graph 
  
    
      
        G
        =
        (
        V
        ,
        E
        )
      
    
    {\\displaystyle G=(V,E)}
  
, with vertex set 
  
    
      
        V
      
    
    {\\displaystyle V}
  
 and edge set 
  
    
      
        E
      
    
    {\\displaystyle E}
  
, the reachability relation of 
  
    
      
        G
      
    
    {\\displaystyle G}
  
 is the transitive closure of 
  
    
      
        E
      
    
    {\\displaystyle E}
  
, which is to say the set of all ordered pairs 
  
    
      
        (
        s
        ,
        t
        )
      
    
    {\\displaystyle (s,t)}
  
 of vertices in 
  
    
      
        V
      
    
    {\\displaystyle V}
  
 for which there exists a sequence of vertices 
  
    
      
        
          v
          
            0
          
        
        =
        s
        ,
        
          v
          
            1
          
        
        ,
        
          v
          
            2
          
        
        ,
        .
        .
        .
        ,
        
          v
          
            k
          
        
        =
        t
      
    
    {\\displaystyle v_{0}=s,v_{1},v_{2},...,v_{k}=t}
  
 such that the edge 
  
    
      
        (
        
          v
          
            i
            −
            1
          
        
        ,
        
          v
          
            i
          
        
        )
      
    
    {\\displaystyle (v_{i-1},v_{i})}
  
 is in 
  
    
      
        E
      
    
    {\\displaystyle E}
  
 for all 
  
    
      
        1
        ≤
        i
        ≤
        k
      
    
    {\\displaystyle 1\\leq i\\leq k}
  
.
If 
  
    
      
        G
      
    
    {\\displaystyle G}
  
 is acyclic, then its reachability relation is a partial order; any partial order may be defined in this way, for instance as the reachability relation of its transitive reduction. A noteworthy consequence of this is that since partial orders are anti-symmetric, if 
  
    
      
        s
      
    
    {\\displaystyle s}
  
 can reach 
  
    
      
        t
      
    
    {\\displaystyle t}
  
, then we know that 
  
    
      
        t
      
    
    {\\displaystyle t}
  
 cannot reach 
  
    
      
        s
      
    
    {\\displaystyle s}
  
. Intuitively, if we could travel from 
  
    
      
        s
      
    
    {\\displaystyle s}
  
 to 
  
    
      
        t
      
    
    {\\displaystyle t}
  
 and back to 
  
    
      
        s
      
    
    {\\displaystyle s}
  
, then 
  
    
      
        G
      
    
    {\\displaystyle G}
  
 would contain a cycle, contradicting that it is acyclic.
If 
  
    
      
        G
      
    
    {\\displaystyle G}
  
 is directed but not acyclic (i.e. it contains at least one cycle), then its reachability relation will correspond to a preorder instead of a partial order.


== Algorithms ==
Algorithms for determining reachability fall into two classes: those that require preprocessing and those that do not.
If you have only one (or a few) queries to make, it may be more efficient to forgo the use of more complex data structures and compute the reachability of the desired pair directly.  This can be accomplished in linear time using algorithms such as breadth first search or iterative deepening depth-first search.
If you will be making many queries, then a more sophisticated method may be used; the exact choice of method depends on the nature of the graph being analysed. In exchange for preprocessing time and some extra storage space, we can create a data structure which can then answer reachability queries on any pair of vertices in as low as 
  
    
      
        O
        (
        1
        )
      
    
    {\\displaystyle O(1)}
  
 time.  Three different algorithms and data structures for three different, increasingly specialized situations are outlined below.


=== Floyd–Warshall Algorithm ===
The Floyd–Warshall algorithm can be used to compute the transitive closure of any directed graph, which gives rise to the reachability relation as in the definition, above.
The algorithm requires 
  
    
      
        O
        (
        
          |
        
        V
        
          
            |
          
          
            3
          
        
        )
      
    
    {\\displaystyle O(|V|^{3})}
  
 time and 
  
    
      
        O
        (
        
          |
        
        V
        
          
            |
          
          
            2
          
        
        )
      
    
    {\\displaystyle O(|V|^{2})}
  
 space in the worst case. This algorithm is not solely interested in reachability as it also computes the shortest path distance between all pairs of vertices. For graphs containing negative cycles, shortest paths may be undefined, but reachability between pairs can still be noted.


=== Thorup's Algorithm ===
For planar digraphs, a much faster method is available, as described by Mikkel Thorup in 2004. This method can answer reachability queries on a planar graph in 
  
    
      
        O
        (
        1
        )
      
    
    {\\displaystyle O(1)}
  
 time after spending 
  
    
      
        O
        (
        n
        log
        ⁡
        
          n
        
        )
      
    
    {\\displaystyle O(n\\log {n})}
  
 preprocessing time to create a data structure of 
  
    
      
        O
        (
        n
        log
        ⁡
        
          n
        
        )
      
    
    {\\displaystyle O(n\\log {n})}
  
 size. This algorithm can also supply approximate shortest path distances, as well as route information.
The overall approach is to associate with each vertex a relatively small set of so-called separator paths such that any path from a vertex 
  
    
      
        v
      
    
    {\\displaystyle v}
  
 to any other vertex 
  
    
      
        w
      
    
    {\\displaystyle w}
  
 must go through at least one of the separators associated with 
  
    
      
        v
      
    
    {\\displaystyle v}
  
 or 
  
    
      
        w
      
    
    {\\displaystyle w}
  
.""",
    tier=2,
    domain="graph_theory",
    source="Wikipedia, 'Reachability'",
    source_url="https://en.wikipedia.org/wiki/Reachability",
))

register_atom(Atom(
    atom_type="theorem",
    name="integral",
    content="""In mathematics, an integral is the continuous analog of a sum, and is used to calculate areas, volumes, and their generalizations. The process of computing an integral, called integration, is one of the two fundamental operations of calculus, along with differentiation. Integration was initially used to solve problems in mathematics and physics, such as finding the area under a curve, or determining displacement from velocity. Usage of integration expanded to a wide variety of scientific fields thereafter.
A definite integral computes the signed area of the region in the plane that is bounded by the graph of a given function between two points in the real line. Conventionally, areas above the horizontal axis of the plane are positive while areas below are negative. Integrals also refer to the concept of an antiderivative, a function whose derivative is the given function; in this case, they are also called indefinite integrals. The fundamental theorem of calculus relates definite integration to differentiation and provides a method to compute the definite integral of a function when its antiderivative is known; differentiation and integration are inverse operations.
Although methods of calculating areas and volumes dated from ancient Greek mathematics, the principles of integration were formulated independently by Isaac Newton and Gottfried Wilhelm Leibniz in the late 17th century, who thought of the area under a curve as an infinite sum of rectangles of infinitesimal width. Bernhard Riemann later gave a rigorous definition of integrals, which is based on a limiting procedure that approximates the area of a curvilinear region by breaking the region into infinitesimally thin vertical slabs. In the early 20th century, Henri Lebesgue generalized Riemann's formulation by introducing what is now referred to as the Lebesgue integral; it is more general than Riemann's in the sense that a wider class of functions are Lebesgue-integrable.
Integrals may be generalized depending on the type of the function as well as the domain over which the integration is performed. For example, a line integral is defined for functions of two or more variables, and the interval of integration is replaced by a curve connecting two points in space. In a surface integral, the curve is replaced by a piece of a surface in three-dimensional space.


== History ==


=== Pre-calculus integration ===
The first documented systematic technique capable of determining integrals is the method of exhaustion of the ancient Greek astronomer Eudoxus and philosopher Democritus (ca. 370 BC), which sought to find areas and volumes by breaking them up into an infinite number of divisions for which the area or volume was known. This method was further developed and employed by Archimedes in the 3rd century BC and used to calculate the area of a circle, the surface area and volume of a sphere, area of an ellipse, the area under a parabola, the volume of a segment of a paraboloid of revolution, the volume of a segment of a hyperboloid of revolution, and the area of a spiral.
A similar method was independently developed in China around the 3rd century AD by Liu Hui, who used it to find the area of the circle. This method was later used in the 5th century by Chinese father-and-son mathematicians Zu Chongzhi and Zu Geng to find the volume of a sphere.
In the Middle East, Hasan Ibn al-Haytham, Latinized as Alhazen (c. 965 – c. 1040 AD) derived a formula for the sum of fourth powers. Alhazen determined the equations to calculate the area enclosed by the curve represented by 
  
    
      
        y
        =
        
          x
          
            k
          
        
      
    
    {\\displaystyle y=x^{k}}
  
 (which translates to the integral 
  
    
      
        ∫
        
          x
          
            k
          
        
        
        d
        x
      
    
    {\\displaystyle \\int x^{k}\\,dx}
  
 in contemporary notation), for any given non-negative integer value of 
  
    
      
        k
      
    
    {\\displaystyle k}
  
. He used the results to carry out what would now be called an integration of this function, where the formulae for the sums of integral squares and fourth powers allowed him to calculate the volume of a paraboloid.
The next significant advances in integral calculus did not begin to appear until the 17th century. At this time, the work of Cavalieri with his method of indivisibles, and work by Fermat, began to lay the foundations of modern calculus, with Cavalieri computing the integrals of xn up to degree n = 9 in Cavalieri's quadrature formula. The case n = −1 required the invention of a function, the hyperbolic logarithm, achieved by quadrature of the hyperbola in 1647.
Further steps were made in the early 17th century by Barrow and Torricelli, who provided the first hints of a connection between integration and differentiation. Barrow provided the first proof of the fundamental theorem of calculus. Wallis generalized Cavalieri's method, computing integrals of x to a general power, including negative powers and fractional powers.


=== Leibniz and Newton ===
The major advance in integration came in the 17th century with the independent discovery of the fundamental theorem of calculus by Leibniz and Newton. The theorem demonstrates a connection between integration and differentiation. This connection, combined with the comparative ease of differentiation, can be exploited to calculate integrals. In particular, the fundamental theorem of calculus allows one to solve a much broader class of problems. Equal in importance is the comprehensive mathematical framework that both Leibniz and Newton developed. Given the name infinitesimal calculus, it allowed for precise analysis of functions with continuous domains. This framework eventually became modern calculus, whose notation for integrals is drawn directly from the work of Leibniz.


=== Formalization ===
While Newton and Leibniz provided a systematic approach to integration, their work lacked a degree of rigour. Bishop Berkeley memorably attacked the vanishing increments used by Newton, calling them "ghosts of departed quantities". Calculus acquired a firmer footing with the development of limits. Integration was first rigorously formalized, using limits, by Riemann. Although all bounded piecewise continuous functions are Riemann-integrable on a bounded interval, subsequently more general functions were considered—particularly in the context of Fourier analysis—to which Riemann's definition does not apply, and Lebesgue formulated a different definition of integral, founded in measure theory (a subfield of real analysis). Other definitions of integral, extending Riemann's and Lebesgue's approaches, were proposed. These approaches based on the real number system are the ones most common today, but alternative approaches exist, such as a definition of integral as the standard part of an infinite Riemann sum, based on the hyperreal number system.


=== Historical notation ===
The notation for the indefinite integral was introduced by Gottfried Wilhelm Leibniz in 1675. He adapted the integral symbol, ∫, from the letter ſ (long s), standing for summa (written as ſumma; Latin for "sum" or "total"). The modern notation for the definite integral, with limits above and below the integral sign, was first used by Joseph Fourier in Mémoires of the French Academy around 1819–1820, reprinted in his book of 1822.
Isaac Newton used a small vertical bar above a variable to indicate integration, or placed the variable inside a box.""",
    tier=3,
    domain="calculus",
    source="Wikipedia, 'Integral'",
    source_url="https://en.wikipedia.org/wiki/Integral",
))

register_atom(Atom(
    atom_type="theorem",
    name="second_derivative",
    content="""In calculus, the second derivative, or the second-order derivative, of a function f is the derivative of the derivative of f. Informally, the second derivative can be phrased as "the rate of change of the rate of change"; for example, the second derivative of the position of an object with respect to time is the instantaneous acceleration of the object, or the rate at which the velocity of the object is changing with respect to time. In Leibniz notation:

  
    
      
        a
        =
        
          
            
              d
              v
            
            
              d
              t
            
          
        
        =
        
          
            
              
                d
                
                  2
                
              
              x
            
            
              d
              
                t
                
                  2
                
              
            
          
        
        ,
      
    
    {\\displaystyle a={\\frac {dv}{dt}}={\\frac {d^{2}x}{dt^{2}}},}
  

where a is acceleration, v is velocity, t is time, x is position, and d is the instantaneous "delta" or change. The last expression 
  
    
      
        
          
            
              
                
                  d
                  
                    2
                  
                
                x
              
              
                d
                
                  t
                  
                    2
                  
                
              
            
          
        
      
    
    {\\displaystyle {\\tfrac {d^{2}x}{dt^{2}}}}
  
 is the second derivative of position (x) with respect to time.
On the graph of a function, the second derivative corresponds to the curvature or concavity of the graph. The graph of a function with a positive second derivative is upwardly concave, while the graph of a function with a negative second derivative curves in the opposite way.


== Second derivative power rule ==
The power rule for the first derivative, if applied twice, will produce the second derivative power rule as follows:

  
    
      
        
          
            
              d
              
                2
              
            
            
              d
              
                x
                
                  2
                
              
            
          
        
        
          x
          
            n
          
        
        =
        
          
            d
            
              d
              x
            
          
        
        
          
            d
            
              d
              x
            
          
        
        
          x
          
            n
          
        
        =
        
          
            d
            
              d
              x
            
          
        
        
          (
          
            n
            
              x
              
                n
                −
                1
              
            
          
          )
        
        =
        n
        
          
            d
            
              d
              x
            
          
        
        
          x
          
            n
            −
            1
          
        
        =
        n
        (
        n
        −
        1
        )
        
          x
          
            n
            −
            2
          
        
        .
      
    
    {\\displaystyle {\\frac {d^{2}}{dx^{2}}}x^{n}={\\frac {d}{dx}}{\\frac {d}{dx}}x^{n}={\\frac {d}{dx}}\\left(nx^{n-1}\\right)=n{\\frac {d}{dx}}x^{n-1}=n(n-1)x^{n-2}.}
  


== Notation ==

The second derivative of a function 
  
    
      
        f
        (
        x
        )
      
    
    {\\displaystyle f(x)}
  
 is usually denoted 
  
    
      
        
          f
          ″
        
        (
        x
        )
      
    
    {\\displaystyle f''(x)}
  
. That is:

  
    
      
        
          f
          ″
        
        =
        
          
            (
            
              f
              ′
            
            )
          
          ′
        
      
    
    {\\displaystyle f''=\\left(f'\\right)'}
  

When using Leibniz's notation for derivatives, the second derivative of a dependent variable y with respect to an independent variable x is written

  
    
      
        
          
            
              
                d
                
                  2
                
              
              y
            
            
              d
              
                x
                
                  2
                
              
            
          
        
        .
      
    
    {\\displaystyle {\\frac {d^{2}y}{dx^{2}}}.}
  

This notation is derived from the following formula:

  
    
      
        
          
            
              
                d
                
                  2
                
              
              y
            
            
              d
              
                x
                
                  2
                
              
            
          
        
        
        =
        
        
          
            d
            
              d
              x
            
          
        
        
          (
          
            
              
                d
                y
              
              
                d
                x
              
            
          
          )
        
        .
      
    
    {\\displaystyle {\\frac {d^{2}y}{dx^{2}}}\\,=\\,{\\frac {d}{dx}}\\left({\\frac {dy}{dx}}\\right).}
  


== Example ==
Given the function

  
    
      
        f
        (
        x
        )
        =
        
          x
          
            3
          
        
        ,
      
    
    {\\displaystyle f(x)=x^{3},}
  

the derivative of f is the function

  
    
      
        
          f
          ′
        
        (
        x
        )
        =
        3
        
          x
          
            2
          
        
        .
      
    
    {\\displaystyle f'(x)=3x^{2}.}
  

The second derivative of f is the derivative of 
  
    
      
        
          f
          ′
        
      
    
    {\\displaystyle f'}
  
, namely

  
    
      
        
          f
          ″
        
        (
        x
        )
        =
        6
        x
        .
      
    
    {\\displaystyle f''(x)=6x.}
  


== Relation to the graph ==


=== Concavity ===
The second derivative of a function f can be used to determine the concavity of the graph of f.  A function whose second derivative is positive is said to be concave up (also referred to as convex), meaning that the tangent line near the point where it touches the function will lie below the graph of the function.  Similarly, a function whose second derivative is negative will be concave down (sometimes simply called concave), and its tangent line will lie above the graph of the function near the point of contact.


=== Inflection points ===

If the second derivative of a function changes sign, the graph of the function will switch from concave down to concave up, or vice versa.  A point where this occurs is called an inflection point.  Assuming the second derivative is continuous, it must take a value of zero at any inflection point, although not every point where the second derivative is zero is necessarily a point of inflection.


=== Second derivative test ===

The relation between the second derivative and the graph can be used to test whether a stationary point for a function (i.e., a point where 
  
    
      
        
          f
          ′
        
        (
        x
        )
        =
        0
      
    
    {\\displaystyle f'(x)=0}
  
) is a local maximum or a local minimum.""",
    tier=3,
    domain="calculus",
    source="Wikipedia, 'Second derivative'",
    source_url="https://en.wikipedia.org/wiki/Second_derivative",
))

register_atom(Atom(
    atom_type="theorem",
    name="determinant",
    content="""In mathematics, the determinant is a scalar-valued function of the entries of a square matrix. The determinant of a matrix A is commonly denoted det(A), det A, or |A|. Its value characterizes some properties of the matrix and the linear map represented, on a given basis, by the matrix. In particular, the determinant is nonzero if and only if the matrix is invertible and the corresponding linear map is an isomorphism. However, if the determinant is zero, the matrix is referred to as singular, meaning it does not have an inverse.
The determinant is completely determined by the two following properties: the determinant of a product of matrices is the product of their determinants, and the determinant of a triangular matrix is the product of its diagonal entries.
The determinant of a 2 × 2 matrix is

  
    
      
        
          
            |
            
              
                
                  a
                
                
                  b
                
              
              
                
                  c
                
                
                  d
                
              
            
            |
          
        
        =
        a
        d
        −
        b
        c
        ,
      
    
    {\\displaystyle {\\begin{vmatrix}a&b\\\\c&d\\end{vmatrix}}=ad-bc,}
  

and the determinant of a 3 × 3 matrix is

  
    
      
        
          
            |
            
              
                
                  a
                
                
                  b
                
                
                  c
                
              
              
                
                  d
                
                
                  e
                
                
                  f
                
              
              
                
                  g
                
                
                  h
                
                
                  i
                
              
            
            |
          
        
        =
        a
        e
        i
        +
        b
        f
        g
        +
        c
        d
        h
        −
        c
        e
        g
        −
        b
        d
        i
        −
        a
        f
        h
        .
      
    
    {\\displaystyle {\\begin{vmatrix}a&b&c\\\\d&e&f\\\\g&h&i\\end{vmatrix}}=aei+bfg+cdh-ceg-bdi-afh.}
  

The determinant of an n × n matrix can be defined in several equivalent ways, the most common being the Leibniz formula, which expresses the determinant as a sum of 
  
    
      
        n
        !
      
    
    {\\displaystyle n!}
  
 (the factorial of n) signed products of matrix entries. It can be computed by the Laplace expansion, which expresses the determinant as a linear combination of determinants of submatrices, or with Gaussian elimination, which allows computing a row echelon form with the same determinant, equal to the product of the diagonal entries of the row echelon form.
Determinants can also be defined by some of their properties. Namely, the determinant is the unique function defined on the n × n matrices that has the four following properties: 

The determinant of the identity matrix is 1.
The exchange of two rows multiplies the determinant by −1.
Multiplying a row by a number multiplies the determinant by this number.
Adding a multiple of one row to another row does not change the determinant.
The above properties relating to rows (properties 2–4) may be replaced by the corresponding statements with respect to columns.
The determinant is invariant under matrix similarity. This implies that, given a linear endomorphism of a finite-dimensional vector space, the determinant of the matrix that represents it on a basis does not depend on the chosen basis. This allows defining the determinant of a linear endomorphism, which does not depend on the choice of a coordinate system.
Determinants occur throughout mathematics. For example, a matrix is often used to represent the coefficients in a system of linear equations, and determinants can be used to solve these equations (Cramer's rule), although other methods of solution are computationally much more efficient. Determinants are used for defining the characteristic polynomial of a square matrix, whose roots are the eigenvalues. In geometry, the signed n-dimensional volume of a n-dimensional parallelepiped is expressed by a determinant, and the determinant of a linear endomorphism determines how the orientation and the n-dimensional volume are transformed under the endomorphism. This is used in calculus with exterior differential forms and the Jacobian determinant, in particular for changes of variables in multiple integrals.


== Two by two matrices ==
The determinant of a 2 × 2 matrix 
  
    
      
        
          
            (
            
              
                
                  a
                
                
                  b
                
              
              
                
                  c
                
                
                  d
                
              
            
            )
          
        
      
    
    {\\displaystyle {\\begin{pmatrix}a&b\\\\c&d\\end{pmatrix}}}
  
 is denoted either by "det" or by vertical bars around the matrix, and is defined as

  
    
      
        det
        
          
            (
            
              
                
                  a
                
                
                  b
                
              
              
                
                  c
                
                
                  d
                
              
            
            )
          
        
        =
        
          
            |
            
              
                
                  a
                
                
                  b
                
              
              
                
                  c
                
                
                  d
                
              
            
            |
          
        
        =
        a
        d
        −
        b
        c
        .
      
    
    {\\displaystyle \\det {\\begin{pmatrix}a&b\\\\c&d\\end{pmatrix}}={\\begin{vmatrix}a&b\\\\c&d\\end{vmatrix}}=ad-bc.}
  

For example,

  
    
      
        det
        
          
            (
            
              
                
                  3
                
                
                  7
                
              
              
                
                  1
                
                
                  −
                  4
                
              
            
            )
          
        
        =
        
          
            |
            
              
                
                  3
                
                
                  7
                
              
              
                
                  1
                
                
                  
                    −
                    4
                  
                
              
            
            |
          
        
        =
        (
        3
        ⋅
        (
        −
        4
        )
        )
        −
        (
        7
        ⋅
        1
        )
        =
        −
        19.
      
    
    {\\displaystyle \\det {\\begin{pmatrix}3&7\\\\1&-4\\end{pmatrix}}={\\begin{vmatrix}3&7\\\\1&{-4}\\end{vmatrix}}=(3\\cdot (-4))-(7\\cdot 1)=-19.}
  


=== First properties ===
The determinant has several key properties that can be proved by direct evaluation of the definition for 
  
    
      
        2
        ×
        2
      
    
    {\\displaystyle 2\\times 2}
  
-matrices, and that continue to hold for determinants of larger matrices.""",
    tier=3,
    domain="linear_algebra",
    source="Wikipedia, 'Determinant'",
    source_url="https://en.wikipedia.org/wiki/Determinant",
))

register_atom(Atom(
    atom_type="definition",
    name="collatz",
    content="""The Collatz conjecture is one of the most famous unsolved problems in mathematics. The conjecture asks whether repeating two simple arithmetic operations will eventually transform every positive integer into 1. It concerns sequences of integers in which each term is obtained from the previous term as follows: if a term is even, the next term is one half of it. If a term is odd, the next term is 3 times the previous term plus 1. The conjecture is that these sequences always reach 1, no matter which positive integer is chosen to start the sequence. The conjecture has been shown to hold for all positive integers up to 2.36×1021, but no general proof has been found.
It is named after the mathematician Lothar Collatz, who introduced the idea in 1937, two years after receiving his doctorate. The sequence of numbers involved is sometimes referred to as the hailstone sequence, hailstone numbers or hailstone numerals (because the values are usually subject to multiple descents and ascents like hailstones in a cloud), or as wondrous numbers.
Paul Erdős said about the Collatz conjecture: "Mathematics may not be ready for such problems." Jeffrey Lagarias stated in 2010 that the Collatz conjecture "is an extraordinarily difficult problem, completely out of reach of present day mathematics". However, though the Collatz conjecture itself remains open, efforts to solve the problem have led to new techniques and many partial results.


== Statement of the problem ==

Consider the following operation on an arbitrary positive integer:

If the number is even, divide it by two.
If the number is odd, triple it and add one.
In modular arithmetic notation, define the function f as follows:

  
    
      
        f
        (
        n
        )
        =
        
          
            {
            
              
                
                  n
                  
                    /
                  
                  2
                
                
                  
                    if 
                  
                  n
                  ≡
                  0
                  
                    
                    (
                    mod
                    
                    2
                    )
                  
                  ,
                
              
              
                
                  3
                  n
                  +
                  1
                
                
                  
                    if 
                  
                  n
                  ≡
                  1
                  
                    
                    (
                    mod
                    
                    2
                    )
                  
                  .
                
              
            
            
          
        
      
    
    {\\displaystyle f(n)={\\begin{cases}n/2&{\\text{if }}n\\equiv 0{\\pmod {2}},\\\\3n+1&{\\text{if }}n\\equiv 1{\\pmod {2}}.\\end{cases}}}
  

Now form a sequence by performing this operation repeatedly, beginning with any positive integer, and taking the result at each step as the input at the next.
In notation:

  
    
      
        
          a
          
            i
          
        
        =
        
          
            {
            
              
                
                  n
                
                
                  
                    for 
                  
                  i
                  =
                  0
                  ,
                
              
              
                
                  f
                  (
                  
                    a
                    
                      i
                      −
                      1
                    
                  
                  )
                
                
                  
                    for 
                  
                  i
                  >
                  0
                
              
            
            
          
        
      
    
    {\\displaystyle a_{i}={\\begin{cases}n&{\\text{for }}i=0,\\\\f(a_{i-1})&{\\text{for }}i>0\\end{cases}}}
  

(that is: ai is the value of f applied to n recursively i times;  ai = f i(n)).
The Collatz conjecture is: This process will eventually reach the number 1, regardless of which positive integer is chosen initially. That is, for each 
  
    
      
        n
      
    
    {\\displaystyle n}
  
, there is some 
  
    
      
        i
      
    
    {\\displaystyle i}
  
 with 
  
    
      
        
          a
          
            i
          
        
        =
        1
      
    
    {\\displaystyle a_{i}=1}
  
.
If the conjecture is false, it can only be because there is some starting number which gives rise to a sequence that does not contain 1. Such a sequence would either enter a repeating cycle that excludes 1, or increase without bound. No such sequence has been found.
The smallest i such that ai < a0  is called the stopping time of n. Similarly, the smallest k such that ak = 1 is called the total stopping time of n. If one of the indexes i or k does not exist, we say that the stopping time or the total stopping time, respectively, is infinite.
The Collatz conjecture asserts that the total stopping time of every n is finite.""",
    tier=3,
    domain="number_theory",
    source="Wikipedia, 'Collatz conjecture'",
    source_url="https://en.wikipedia.org/wiki/Collatz_conjecture",
))

register_atom(Atom(
    atom_type="algorithm",
    name="base_conversion",
    content="""Positional notation, also known as place-value notation, is the property of a numeral system that the value represented by each symbol in a written numeral depends not only on its appearance but also on its position. Each symbol fits in a specific place or position, representing a power of a fixed base. The most common numeral system used today, the Hindu–Arabic numeral system, is a positional system in base ten; each of ten numerical digits is a distinct symbol representing one the numbers zero through nine, and in the context of the full numeral, each symbol's value is the digit multiplied by a power of ten.
Most early numeral systems, such as Roman numerals, are essentially based on the additive principle: each symbol type represents one fixed value, and the value of a numeral is the sum of the values of the separate symbols. For example, the Roman numeral CCXXVIII has two copies of the symbol C meaning 100, two copies of X meaning 10, one V meaning 5, and three copies of I meaning 1, so overall represents the number 100 + 100 + 10 + 10 + 5 + 1 + 1 + 1 = 228; by comparison, the equivalent Hindu–Arabic numeral, 228, consists of the symbol 2 representing 2 × 100, another symbol 2 representing 2 × 10, and finally an 8 representing 8 × 1.
The Babylonian numeral system, base 60, was the first positional system to be developed, and its influence is present today in the way time and angles are counted in tallies related to 60, such as 60 minutes in an hour and 360 degrees in a circle. The Inca used knots tied in a decimal positional system to store numbers and other values in quipu cords.
The binary numeral system (base two) is used in almost all computers and electronic devices because it is easier to implement efficiently in electronic circuits.
Systems with negative base, complex base or negative digits have been described. Most of them do not require a minus sign for designating negative numbers.
The use of a radix point (decimal point in base ten), extends to include fractions and allows the representation of any real number with arbitrary accuracy. With positional notation, arithmetical computations are much simpler than with any older numeral system; this led to the rapid spread of the notation when it was introduced in western Europe.


== History ==

Today, the base-10 (decimal) system, which is presumably motivated by counting with the ten fingers, is ubiquitous. Other bases have been used in the past, and some continue to be used today. For example, the Babylonian numeral system, credited as the first positional numeral system, was base-60. However, it lacked a real zero. Initially inferred only from context, later, by about 700 BC, zero came to be indicated by a "space" or a "punctuation symbol" (such as two slanted wedges) between numerals. It was a placeholder rather than a true zero because it was not used alone or at the end of a number. Numbers like 2 and 120 (2×60) looked the same because the larger number lacked a final placeholder. Only context could differentiate them.
The polymath Archimedes (ca. 287–212 BC) invented a decimal positional system based on 108 in his Sand Reckoner; 19th century German mathematician Carl Gauss lamented how science might have progressed had Archimedes only made the leap to something akin to the modern decimal system. Hellenistic and Roman astronomers used a base-60 system based on the Babylonian model (see Greek numerals § Zero).
Before positional notation became standard, simple additive systems (sign-value notation) such as Roman numerals or Chinese numerals were used, and accountants in the past used the abacus or stone counters to do arithmetic until the introduction of positional notation.

Counting rods and most abacuses have been used to represent numbers in a positional numeral system. With counting rods or abacus to perform arithmetic operations, the writing of the starting, intermediate and final values of a calculation could easily be done with a simple additive system in each position or column. This approach required no memorization of tables (as does positional notation) and could produce practical results quickly.
The oldest extant positional notation system is either that of Chinese rod numerals, used from at least the early 8th century, or perhaps Khmer numerals, showing possible usages of positional-numbers in the 7th century. Khmer numerals and other Indian numerals originate with the Brahmi numerals of about the 3rd century BC, which symbols were, at the time, not used positionally. Medieval Indian numerals are positional, as are the derived Arabic numerals, recorded from the 10th century.
After the French Revolution (1789–1799), the new French government promoted the extension of the decimal system. Some of those pro-decimal efforts—such as decimal time and the decimal calendar—were unsuccessful. Other French pro-decimal efforts—currency decimalisation and the metrication of weights and measures—spread widely out of France to almost the whole world.


=== History of positional fractions ===

Decimal fractions were first developed and used by the Chinese in the form of rod calculus in the 1st century BC, and then spread to the rest of the world. J. Lennart Berggren notes that positional decimal fractions were being used in Damascus by mathematician Abu'l-Hasan al-Uqlidisi in the mid 10th century. The Jewish mathematician Immanuel Bonfils used decimal fractions around 1350, but did not develop any notation to represent them. The Persian mathematician Jamshīd al-Kāshī similarly adopted their use in the 15th century. Al Khwarizmi introduced fractions to Islamic countries in the early 9th century; his fraction presentation was similar to the traditional Chinese mathematical fractions from Sunzi Suanjing. This form of fraction with numerator on top and denominator at bottom without a horizontal bar was also used by 10th century Abu'l-Hasan al-Uqlidisi and 15th century Jamshīd al-Kāshī's work "Arithmetic Key".

The adoption of the decimal representation of numbers less than one, a fraction, is often credited to Simon Stevin through his textbook De Thiende; but both Stevin and E. J. Dijksterhuis indicate that Regiomontanus contributed to the European adoption of general decimals:

European mathematicians, when taking over from the Hindus, via the Arabs, the idea of positional value for integers, neglected to extend this idea to fractions. For some centuries they confined themselves to using common and sexagesimal fractions ... This half-heartedness has never been completely overcome, and sexagesimal fractions still form the basis of our trigonometry, astronomy and measurement of time.
... Mathematicians sought to avoid fractions by taking the radius R equal to a number of units of length of the form 10n and then assuming for n so great an integral value that all occurring quantities could be expressed with sufficient accuracy by integers.

The first to apply this method was the German astronomer Regiomontanus. To the extent that he expressed goniometrical line-segments in a unit R/10n, Regiomontanus may be called an anticipator of the doctrine of decimal positional fractions.
In the estimation of Dijksterhuis, "after the publication of De Thiende only a small advance was required to establish the complete system of decimal positional fractions, and this step was taken promptly by a number of writers ... next to Stevin the most important figure in this development was Regiomontanus." Dijksterhuis noted that [Stevin] "gives full credit to Regiomontanus for his prior contribution, saying that the trigonometric tables of the German astronomer actually contain the whole theory of 'numbers of the tenth progress'."


== Mathematics ==


=== Base of the numeral system ===
In mathematical numeral systems the radix r is usually the number of unique digits, including zero, that a positional numeral system uses to represent numbers.""",
    tier=3,
    domain="number_theory",
    source="Wikipedia, 'Positional notation'",
    source_url="https://en.wikipedia.org/wiki/Positional_notation",
))

register_atom(Atom(
    atom_type="algorithm",
    name="prefix_scan",
    content="""In computer science, the prefix sum, cumulative sum, inclusive scan, or simply scan of a sequence of numbers x0, x1, x2, ... is a second sequence of numbers y0, y1, y2, ..., the sums of prefixes (running totals) of the input sequence:

y0 = x0
y1 = x0 + x1
y2 = x0 + x1+ x2
...
For instance, the prefix sums of the natural numbers are the triangular numbers:

Prefix sums are trivial to compute in sequential models of computation, by using the formula yi = yi − 1 + xi to compute each output value in sequence order. However, despite their ease of computation, prefix sums are a useful primitive in certain algorithms such as counting sort,
and they form the basis of the scan higher-order function in functional programming languages. Prefix sums have also been much studied in parallel algorithms, both as a test problem to be solved and as a useful primitive to be used as a subroutine in other parallel algorithms.
Abstractly, a prefix sum requires only a binary associative operator ⊕, making it useful for many applications from calculating well-separated pair decompositions of points to string processing.
Mathematically, the operation of taking prefix sums can be generalized from finite to infinite sequences; in that context, a prefix sum is known as a partial sum of a series. Prefix summation or partial summation form linear operators on the vector spaces of finite or infinite sequences; their inverses are finite difference operators.


== Scan higher order function ==
In functional programming terms, the prefix sum may be generalized to any binary operation (not just the addition operation); the higher order function resulting from this generalization is called a scan, and it is closely related to the fold operation. Both the scan and the fold operations apply the given binary operation to the same sequence of values, but differ in that the scan returns the whole sequence of results from the binary operation, whereas the fold returns only the final result. For instance, the sequence of factorial numbers may be generated by a scan of the natural numbers using multiplication instead of addition:


=== Inclusive and exclusive scans ===

Programming language and library implementations of scan may be either inclusive or exclusive. An inclusive scan includes input xi when computing output yi (i.e., 
  
    
      
        
          y
          
            i
          
        
        =
        
          ⨁
          
            j
            =
            0
          
          
            i
          
        
        
          x
          
            j
          
        
      
    
    {\\textstyle y_{i}=\\bigoplus _{j=0}^{i}x_{j}}
  
) while an exclusive scan does not (i.e., 
  
    
      
        
          y
          
            i
          
        
        =
        
          ⨁
          
            j
            =
            0
          
          
            i
            −
            1
          
        
        
          x
          
            j
          
        
      
    
    {\\textstyle y_{i}=\\bigoplus _{j=0}^{i-1}x_{j}}
  
). In the latter case, implementations either leave y0 undefined or accept a separate "x−1" value with which to seed the scan. Either type of scan can be transformed into the other: an inclusive scan can be transformed into an exclusive scan by shifting the array produced by the scan right by one element and inserting the identity value at the left of the array. Conversely, an exclusive scan be transformed into an inclusive scan by shifting the array produced by the scan left and inserting the sum of the last element of the scan and the last element of the input array at the right of the array.
The following table lists examples of the inclusive and exclusive scan functions provided by a few programming languages and libraries:

The directive-based OpenMP parallel programming model supports both inclusive and exclusive scan support beginning with Version 5.0.


== Parallel algorithms ==
There are two key algorithms for computing a prefix sum in parallel. The first offers a shorter span and more parallelism but is not work-efficient. The second is work-efficient but requires double the span and offers less parallelism. These are presented in turn below.


=== Algorithm 1: Shorter span, more parallel ===

Hillis and Steele present the
following parallel prefix sum algorithm:

for i <- 0 to log2(n) do
    for j <- 0 to n - 1 do in parallel
        if j < 2i then
            xi+1j <- xij
        else
            xi+1j <- xij + xij - 2i

In the above, the notation 
  
    
      
        
          x
          
            j
          
          
            i
          
        
      
    
    {\\displaystyle x_{j}^{i}}
  
 means the value of the jth element of array x in timestep i.
With a single processor this algorithm would run in O(n log n) time. However, if the machine has at least n processors to perform the inner loop in parallel, the algorithm as a whole runs in O(log n) time, the number of iterations of the outer loop.


=== Algorithm 2: Work-efficient ===

A work-efficient parallel prefix sum can be computed by the following steps.

Compute the sums of consecutive pairs of items in which the first item of the pair has an even index: z0 = x0 + x1, z1 = x2 + x3, etc.
Recursively compute the prefix sum w0, w1, w2, ... of the sequence z0, z1, z2, ...
Express each term of the final sequence y0, y1, y2, ... as the sum of up to two terms of these intermediate sequences: y0 = x0, y1 = z0, y2 = z0 + x2, y3 = w1, etc. After the first value, each successive number yi is either copied from a position half as far through the w sequence, or is the previous value added to one value in the x sequence.
If the input sequence has n steps, then the recursion continues to a depth of O(log n), which is also the bound on the parallel running time of this algorithm. The number of steps of the algorithm is O(n), and it can be implemented on a parallel random access machine with O(n/log n) processors without any asymptotic slowdown by assigning multiple indices to each processor in rounds of the algorithm for which there are more elements than processors.


=== Discussion ===
Each of the preceding algorithms runs in O(log n) time. However, the former takes exactly log2 n steps, while the latter requires 2 log2 n − 2 steps. For the 16-input examples illustrated, Algorithm 1 is 12-way parallel (49 units of work divided by a span of 4) while Algorithm 2 is only 4-way parallel (26 units of work divided by a span of 6). However, Algorithm 2 is work-efficient—it performs only a constant factor (2) of the amount of work required by the sequential algorithm—while Algorithm 1 is work-inefficient—it performs asymptotically more work (a logarithmic factor) than is required sequentially. Consequently, Algorithm 1 is likely to perform better when abundant parallelism is available, but Algorithm 2 is likely to perform better when parallelism is more limited.
Parallel algorithms for prefix sums can often be generalized to other scan operations on associative binary operations, and they can also be computed efficiently on modern parallel hardware such as a GPU. The idea of building in hardware a functional unit dedicated to computing multi-parameter prefix-sum was patented by Uzi Vishkin.
Many parallel implementations follow a two pass procedure where partial prefix sums are calculated in the first pass on each processing unit; the prefix sum of these partial sums is then calculated and broadcast back to the processing units for a second pass using the now known prefix as the initial value. Asymptotically this method takes approximately two read operations and one write operation per item.


=== Concrete implementations of prefix sum algorithms ===
An implementation of a parallel prefix sum algorithm, like other parallel algorithms, has to take the parallelization architecture of the platform into account.""",
    tier=3,
    domain="algorithms",
    source="Wikipedia, 'Prefix sum'",
    source_url="https://en.wikipedia.org/wiki/Prefix_sum",
))

register_atom(Atom(
    atom_type="algorithm",
    name="rpn",
    content="""Reverse Polish notation (RPN), also known as reverse Łukasiewicz notation, Polish postfix notation or simply postfix notation, is a mathematical notation in which operators follow their operands, in contrast to the more common infix notation (in which operators are placed between operands), as well as prefix notation (in which operators precede their operands). The notation does not need any parentheses as long as each operator has a fixed number of operands.
The term postfix notation describes the general scheme in mathematics and computer sciences, whereas the term reverse Polish notation typically refers specifically to the method used to enter calculations into hardware or software calculators, which often have additional side effects and implications depending on the actual implementation involving a  stack. The description "Polish" refers to the nationality of logician Jan Łukasiewicz, who invented Polish notation in 1924.
The first computer to use postfix notation, though it long remained essentially unknown outside of Germany, was Konrad Zuse's Z3 in 1941 as well as his Z4 in 1945. The reverse Polish scheme was again proposed in 1954 by Arthur Burks, Don Warren, and Jesse Wright and was independently reinvented by Friedrich L. Bauer and Edsger W. Dijkstra in the early 1960s to reduce computer memory access and use the stack to evaluate expressions. The algorithms and notation for this scheme were extended by the philosopher and computer scientist Charles L. Hamblin in the mid-1950s.
During the 1970s and 1980s, Hewlett-Packard used RPN in all of their desktop and hand-held calculators, and has continued to use it in some models into the 2020s. In computer science, reverse Polish notation is used in stack-oriented programming languages such as Forth, dc, Factor, STOIC, PostScript, RPL, and Joy.


== Explanation ==
In reverse Polish notation, the operators follow their operands. For example, to add 3 and 4 together, the expression is 3 4 + rather than 3 + 4. The conventional notation expression 3 − 4 + 5 becomes 3 (enter) 4 − 5 + in reverse Polish notation: 4 is first subtracted from 3, then 5 is added to it.
The concept of a stack, a last-in/first-out construct, is integral to the left-to-right evaluation of RPN. In the example 3 4 −, first the 3 is put onto the stack, then the 4; the 4 is now on top and the 3 below it. The subtraction operator removes the top two items from the stack, performs 3 − 4, and puts the result of −1 onto the stack.
Common language in this context refers to items being pushed onto the stack when added and popped or removed from the stack when taken off.
The advantage of reverse Polish notation is that it removes the need for order of operations and parentheses that are required by infix notation and can be evaluated linearly, left-to-right. For example, the infix expression (3 + 4) × (5 + 6) becomes 3 4 + 5 6 + × in reverse Polish notation.


== Practical implications ==
Reverse Polish notation has been compared to how one had to work through problems with a slide rule.
In comparison, testing of reverse Polish notation with algebraic notation, reverse Polish has been found to lead to faster calculations, for two reasons. The first reason is that reverse Polish calculators do not need expressions to be parenthesized, so fewer operations need to be entered to perform typical calculations. Additionally, users of reverse Polish calculators made fewer mistakes than for other types of calculators. Later research clarified that the increased speed from reverse Polish notation may be attributed to the smaller number of keystrokes needed to enter this notation, rather than to a smaller cognitive load on its users. However, anecdotal evidence suggests that reverse Polish notation is more difficult for users who previously learned algebraic notation.


== Converting from infix notation ==

Edsger W. Dijkstra invented the shunting-yard algorithm to convert infix expressions to postfix expressions (reverse Polish notation), so named because its operation resembles that of a railroad shunting yard.
There are other ways of producing postfix expressions from infix expressions. Most operator-precedence parsers can be modified to produce postfix expressions; in particular, once an abstract syntax tree has been constructed, the corresponding postfix expression is given by a simple post-order traversal of that tree.


== Implementations ==


=== Hardware calculators ===


==== Early history ====
The first computer implementing a form of reverse Polish notation (but without the name and also without a stack), was Konrad Zuse's Z3, which he started to construct in 1938 and demonstrated publicly on 12 May 1941. In dialog mode, it allowed operators to enter two operands followed by the desired operation. It was destroyed on 21 December 1943 in a bombing raid. With Zuse's help a first replica was built in 1961. The 1945 Z4 also added a 2-level stack.
Other early computers to implement architectures enabling reverse Polish notation were the English Electric Company's KDF9 machine, which was announced in 1960 and commercially available in 1963, and the Burroughs B5000, announced in 1961 and also delivered in 1963:
The KDF9 designers drew ideas from Hamblin's GEORGE (General Order Generator), a high-level programming language written for a DEUCE computer installed at The New South Wales University of Technology, Kensington, Australia, in 1957.
One of the designers of the B5000, Robert S. Barton, later wrote that he developed reverse Polish notation independently of Hamblin sometime in 1958 after reading a 1954 textbook on symbolic logic by Irving Copi, where he found a reference to Polish notation, which made him read the works of Jan Łukasiewicz as well, and before he was aware of Hamblin's work.
Friden introduced reverse Polish notation to the desktop calculator market with the EC-130, designed by Robert "Bob" Appleby Ragen, supporting a four-level stack in June 1963. The successor EC-132 added a square root function in April 1965. Around 1966, the Monroe Epic calculator supported an unnamed input scheme resembling RPN as well.


==== Hewlett-Packard ====

Hewlett-Packard engineers designed the 9100A Desktop Calculator in 1968 with reverse Polish notation with only three stack levels with working registers X ("keyboard"), Y ("accumulate") and visible storage register Z ("temporary"), a reverse Polish notation variant later referred to as three-level RPN. This calculator popularized reverse Polish notation among the scientific and engineering communities.
The HP-35, the world's first handheld scientific calculator, introduced the classical four-level RPN with its specific ruleset of the so-called operational (memory) stack (later also called automatic memory stack) in 1972. In this scheme, the Enter ↑ key duplicates values into Y under certain conditions (automatic stack lift with temporary stack lift disable), and the top register T ("top") gets duplicated on drops (top copy on pop aka top stack level repetition) in order to ease some calculations and to save keystrokes. HP used reverse Polish notation on every handheld calculator it sold, whether scientific, financial, or programmable, until it introduced the HP-10 adding machine calculator in 1977. By this time, HP was the leading manufacturer of calculators for professionals, including engineers and accountants.
Later calculators with LCDs in the early 1980s, such as the HP-10C, HP-11C, HP-15C, HP-16C, and the financial HP-12C calculator also used reverse Polish notation. In 1988, Hewlett-Packard introduced a business calculator, the HP-19B, without reverse Polish notation, but its 1990 successor, the HP-19BII, gave users the option of using algebraic or reverse Polish notation again.
In 1986, HP introduced RPL, an object-oriented successor to reverse Polish notation.""",
    tier=3,
    domain="algorithms",
    source="Wikipedia, 'Reverse Polish notation'",
    source_url="https://en.wikipedia.org/wiki/Reverse_Polish_notation",
))

register_atom(Atom(
    atom_type="algorithm",
    name="cycle_detect",
    content="""In computer science, cycle detection or cycle finding is the algorithmic problem of finding a cycle in a sequence of iterated function values.
For any function f that maps a finite set S to itself, and any initial value x0 in S, the sequence of iterated function values

  
    
      
        
          x
          
            0
          
        
        ,
         
        
          x
          
            1
          
        
        =
        f
        (
        
          x
          
            0
          
        
        )
        ,
         
        
          x
          
            2
          
        
        =
        f
        (
        
          x
          
            1
          
        
        )
        ,
         
        …
        ,
         
        
          x
          
            i
          
        
        =
        f
        (
        
          x
          
            i
            −
            1
          
        
        )
        ,
         
        …
      
    
    {\\displaystyle x_{0},\\ x_{1}=f(x_{0}),\\ x_{2}=f(x_{1}),\\ \\dots ,\\ x_{i}=f(x_{i-1}),\\ \\dots }
  

must eventually use the same value twice: there must be some pair of distinct indices i and j such that xi = xj. Once this happens, the sequence must continue periodically, by repeating the same sequence of values from xi to xj − 1. Cycle detection is the problem of finding i and j, given f and x0.
Several algorithms are known for finding cycles quickly and with little memory. Robert W. Floyd's tortoise and hare algorithm moves two pointers at different speeds through the sequence of values until they both point to equal values. Alternatively, Brent's algorithm is based on the idea of exponential search. Both Floyd's and Brent's algorithms use only a constant number of memory cells, and take a number of function evaluations that is proportional to the distance from the start of the sequence to the first repetition. Several other algorithms trade off larger amounts of memory for fewer function evaluations.
The applications of cycle detection include testing the quality of pseudorandom number generators and cryptographic hash functions, computational number theory algorithms, detection of infinite loops in computer programs and periodic configurations in cellular automata,  automated shape analysis of linked list data structures, and detection of deadlocks for transactions management in DBMS.


== Example ==

The figure shows a function f that maps the set S = {0,1,2,3,4,5,6,7,8} to itself. If one starts from x0 = 2 and repeatedly applies f, one sees the sequence of values

2, 0, 6, 3, 1, 6, 3, 1, 6, 3, 1, ....
The cycle in this value sequence is 6, 3, 1.


== Definitions ==
Let S be any finite set, f be any endofunction from S to itself, and x0 be any element of S. For any i > 0, let xi = f(xi − 1). Let μ be the smallest index such that the value xμ reappears infinitely often within the sequence of values xi, and let λ (the loop length) be the smallest positive integer such that xμ = xλ + μ. The cycle detection problem is the task of finding λ and μ.
One can view the same problem graph-theoretically, by constructing a functional graph (that is, a directed graph in which each vertex has a single outgoing edge) the vertices of which are the elements of S and the edges of which map an element to the corresponding function value, as shown in the figure. The set of vertices reachable from  starting vertex x0 form a subgraph with a shape resembling the Greek letter rho (ρ): a path of length μ from x0 to a cycle of λ vertices.
Practical cycle-detection algorithms do not find λ and μ exactly.  They usually find lower and upper bounds μl ≤ μ ≤ μh for the start of the cycle, and a more detailed search of the range must be performed if the exact value of μ is needed.  Also, most algorithms do not guarantee to find λ directly, but may find some multiple kλ < μ + λ.  (Continuing the search for an additional kλ/q steps, where q is the smallest prime divisor of kλ, will either find the true λ or prove that k = 1.)


== Computer representation ==
Except in toy examples like the above, f will not be specified as a table of values.  Such a table implies O(|S|) space complexity, and if that is permissible, building a predecessor array (associative array mapping xi to i) while iterating f will detect the first repeated value when it is visited the second time, at which point the value in the predecessor array is μ and the current index is μ+λ.  Rather, a cycle detection algorithm is given a black box for generating the sequence xi, and the task is to find λ and μ using very little memory.
The black box might consist of an implementation of the recurrence function f, but it might also store additional internal state to make the computation more efficient.  Although xi = f(xi−1) must be true in principle, this might be expensive to compute directly; the function could be defined in terms of the discrete logarithm of xi−1 or some other difficult-to-compute property which can only be practically computed in terms of additional information.  In such cases, the number of black boxes required becomes a figure of merit distinguishing the algorithms.
A second reason to use one of these algorithms is that they are pointer algorithms which do no operations on elements of S other than testing for equality.  An associative array implementation requires computing a hash function on the elements of S, or ordering them.  But cycle detection can be applied in cases where neither of these are possible.
The classic example is Pollard's rho algorithm for integer factorization, which searches for a factor p of a given number n by looking for values xi and xi+λ which are equal modulo p without knowing p in advance.  This is done by computing the greatest common divisor of the difference xi − xi+λ with a known multiple of p, namely n.  If the gcd is non-trivial (neither 1 nor n), then the value is a proper factor of n, as desired.  If n is not prime, it must have at least one factor p ≤ √n, and by the birthday paradox, a random function f has an expected cycle length (modulo p) of √p ≤ 4√n.


== Algorithms ==
If the input is given as a subroutine for calculating f, the cycle detection problem may be trivially solved using only λ + μ function applications, simply by computing the sequence of values xi and using a data structure such as a hash table to store these values and test whether each subsequent value has already been stored. However, the space complexity of this algorithm is proportional to λ + μ, unnecessarily large. Additionally, to implement this method as a pointer algorithm would require applying the equality test to each pair of values, resulting in quadratic time overall. Thus, research in this area has concentrated on two goals: using less space than this naive algorithm, and finding pointer algorithms that use fewer equality tests.


=== Floyd's tortoise and hare ===

Floyd's cycle-finding algorithm is a pointer algorithm that uses only two pointers, which move through the sequence at different speeds. It is also called the "tortoise and the hare algorithm", alluding to Aesop's fable of The Tortoise and the Hare.
The algorithm is named after Robert W. Floyd, who was credited with its invention by Donald Knuth. However, the algorithm does not appear in Floyd's published work, and this may be a misattribution: Floyd describes algorithms for listing all simple cycles in a directed graph in a 1967 paper, but this paper does not describe the cycle-finding problem in functional graphs that is the subject of this article. In fact, Knuth's statement (in 1969), attributing it to Floyd, without citation, is the first known appearance in print, and it thus may be a folk theorem, not attributable to a single individual.
The key insight in the algorithm is as follows.""",
    tier=3,
    domain="algorithms",
    source="Wikipedia, 'Cycle detection'",
    source_url="https://en.wikipedia.org/wiki/Cycle_detection",
))

register_atom(Atom(
    atom_type="algorithm",
    name="matrix_multiply",
    content="""In mathematics, specifically in linear algebra, matrix multiplication is a binary operation that produces a matrix from two matrices. For matrix multiplication, the number of columns in the first matrix must be equal to the number of rows in the second matrix. The resulting matrix, known as the matrix product, has the number of rows of the first and the number of columns of the second matrix. The product of matrices A and B is denoted as AB.
Matrix multiplication was first described by the French mathematician Jacques Philippe Marie Binet in 1812, to represent the composition of linear maps that are represented by matrices. Matrix multiplication is thus a basic tool of linear algebra, and as such has numerous applications in many areas of mathematics, as well as in applied mathematics, statistics, physics, economics, and engineering.
Computing matrix products is a central operation in all computational applications of linear algebra.


== Notation ==
This article will use the following notational conventions: matrices are represented by capital letters in bold, e.g. A; vectors in lowercase bold, e.g. a; and entries of vectors and matrices are italic (they are numbers from a field), e.g. A and a. Index notation is often the clearest way to express definitions, and is used as standard in the literature. The entry in row i, column j of matrix A is indicated by (A)ij, Aij or aij. In contrast, a single subscript, e.g. A1, A2, is used to select a matrix (not a matrix entry) from a collection of matrices.


== Definitions ==


=== Matrix times matrix ===
If A is an m × n matrix and B is an n × p matrix,

  
    
      
        
          A
        
        =
        
          
            (
            
              
                
                  
                    a
                    
                      11
                    
                  
                
                
                  
                    a
                    
                      12
                    
                  
                
                
                  ⋯
                
                
                  
                    a
                    
                      1
                      n
                    
                  
                
              
              
                
                  
                    a
                    
                      21
                    
                  
                
                
                  
                    a
                    
                      22
                    
                  
                
                
                  ⋯
                
                
                  
                    a
                    
                      2
                      n
                    
                  
                
              
              
                
                  ⋮
                
                
                  ⋮
                
                
                  ⋱
                
                
                  ⋮
                
              
              
                
                  
                    a
                    
                      m
                      1
                    
                  
                
                
                  
                    a
                    
                      m
                      2
                    
                  
                
                
                  ⋯
                
                
                  
                    a
                    
                      m
                      n
                    
                  
                
              
            
            )
          
        
        ,
        
        
          B
        
        =
        
          
            (
            
              
                
                  
                    b
                    
                      11
                    
                  
                
                
                  
                    b
                    
                      12
                    
                  
                
                
                  ⋯
                
                
                  
                    b
                    
                      1
                      p
                    
                  
                
              
              
                
                  
                    b
                    
                      21
                    
                  
                
                
                  
                    b
                    
                      22
                    
                  
                
                
                  ⋯
                
                
                  
                    b
                    
                      2
                      p
                    
                  
                
              
              
                
                  ⋮
                
                
                  ⋮
                
                
                  ⋱
                
                
                  ⋮
                
              
              
                
                  
                    b
                    
                      n
                      1
                    
                  
                
                
                  
                    b
                    
                      n
                      2
                    
                  
                
                
                  ⋯
                
                
                  
                    b
                    
                      n
                      p
                    
                  
                
              
            
            )
          
        
      
    
    {\\displaystyle \\mathbf {A} ={\\begin{pmatrix}a_{11}&a_{12}&\\cdots &a_{1n}\\\\a_{21}&a_{22}&\\cdots &a_{2n}\\\\\\vdots &\\vdots &\\ddots &\\vdots \\\\a_{m1}&a_{m2}&\\cdots &a_{mn}\\\\\\end{pmatrix}},\\quad \\mathbf {B} ={\\begin{pmatrix}b_{11}&b_{12}&\\cdots &b_{1p}\\\\b_{21}&b_{22}&\\cdots &b_{2p}\\\\\\vdots &\\vdots &\\ddots &\\vdots \\\\b_{n1}&b_{n2}&\\cdots &b_{np}\\\\\\end{pmatrix}}}
  

the matrix product C = AB (denoted without multiplication signs or dots) is defined to be the m × p matrix

  
    
      
        
          C
        
        =
        
          
            (
            
              
                
                  
                    c
                    
                      11
                    
                  
                
                
                  
                    c
                    
                      12
                    
                  
                
                
                  ⋯
                
                
                  
                    c
                    
                      1
                      p
                    
                  
                
              
              
                
                  
                    c
                    
                      21
                    
                  
                
                
                  
                    c
                    
                      22
                    
                  
                
                
                  ⋯
                
                
                  
                    c
                    
                      2
                      p
                    
                  
                
              
              
                
                  ⋮
                
                
                  ⋮
                
                
                  ⋱
                
      """,
    tier=4,
    domain="linear_algebra",
    source="Wikipedia, 'Matrix multiplication'",
    source_url="https://en.wikipedia.org/wiki/Matrix_multiplication",
))

register_atom(Atom(
    atom_type="theorem",
    name="matrix_inverse",
    content="""In linear algebra, an invertible matrix (non-singular, non-degenerate or regular) is a square matrix that has an inverse. In other words, if a matrix is invertible, it can be multiplied by its inverse matrix to yield the identity matrix. Invertible matrices are the same size as their inverse.
The inverse of a matrix represents the inverse operation, meaning if a matrix is applied to a particular vector, followed by applying the matrix's inverse, the result is the original vector.


== Definition ==
An n-by-n square matrix A is called invertible if there exists an n-by-n square matrix B such that
  
    
      
        
          A
          B
        
        =
        
          B
          A
        
        =
        
          
            I
          
          
            n
          
        
        ,
      
    
    {\\displaystyle \\mathbf {AB} =\\mathbf {BA} =\\mathbf {I} _{n},}
  
where In denotes the n-by-n identity matrix and the multiplication used is ordinary matrix multiplication. If this is the case, then the matrix B is uniquely determined by A, and is called the inverse of A, denoted by A−1. Matrix inversion is the process of finding the matrix which when multiplied by the original matrix gives the identity matrix.


== Examples ==
Consider the following 2-by-2 matrix:

  
    
      
        
          A
        
        =
        
          
            (
            
              
                
                  −
                  1
                
                
                  
                    
                      
                        3
                        2
                      
                    
                  
                
              
              
                
                  1
                
                
                  −
                  1
                
              
            
            )
          
        
      
    
    {\\displaystyle \\mathbf {A} ={\\begin{pmatrix}-1&{\\tfrac {3}{2}}\\\\1&-1\\end{pmatrix}}}
  

The matrix 
  
    
      
        
          A
        
      
    
    {\\displaystyle \\mathbf {A} }
  
 is invertible, as it has inverse 
  
    
      
        
          B
        
        =
        
          
            (
            
              
                
                  2
                
                
                  3
                
              
              
                
                  2
                
                
                  2
                
              
            
            )
          
        
        ,
      
    
    {\\displaystyle \\mathbf {B} ={\\begin{pmatrix}2&3\\\\2&2\\end{pmatrix}},}
  
 which can be confirmed by computing 

  
    
      
        
          A
        
        
          B
        
        =
        
          
            (
            
              
                
                  −
                  1
                
                
                  
                    
                      
                        3
                        2
                      
                    
                  
                
              
              
                
                  1
                
                
                  −
                  1
                
              
            
            )
          
        
        
          
            (
            
              
                
                  2
                
                
                  3
                
              
              
                
                  2
                
                
                  2
                
              
            
            )
          
        
        =
        
          
            (
            
              
                
                  (
                  −
                  1
                  )
                  ×
                  2
                  +
                  
                    
                      
                        3
                        2
                      
                    
                  
                  ×
                  2
                
                
                  (
                  −
                  1
                  )
                  ×
                  3
                  +
                  
                    
                      
                        3
                        2
                      
                    
                  
                  ×
                  2
                
              
              
                
                  1
                  ×
                  2
                  +
                  (
                  −
                  1
                  )
                  ×
                  2
                
                
                  1
                  ×
                  3
                  +
                  (
                  −
                  1
                  )
                  ×
                  2
                
              
            
            )
          
        
        =
        
          
            (
            
              
                
                  1
                
                
                  0
                
              
              
                
                  0
                
                
                  1
                
              
            
            )
          
        
        =
        
          
            I
          
          
            2
          
        
      
    
    {\\displaystyle \\mathbf {A} \\mathbf {B} ={\\begin{pmatrix}-1&{\\tfrac {3}{2}}\\\\1&-1\\end{pmatrix}}{\\begin{pmatrix}2&3\\\\2&2\\end{pmatrix}}={\\begin{pmatrix}(-1)\\times 2+{\\tfrac {3}{2}}\\times 2&(-1)\\times 3+{\\tfrac {3}{2}}\\times 2\\\\1\\times 2+(-1)\\times 2&1\\times 3+(-1)\\times 2\\end{pmatrix}}={\\begin{pmatrix}1&0\\\\0&1\\end{pmatrix}}=\\mathbf {I} _{2}}
  
 
To check that it is invertible without finding an inverse, 
  
    
      
        det
        
          A
        
        =
        −
        
          
            1
            2
          
        
      
    
    {\\textstyle \\det \\mathbf {A} =-{\\frac {1}{2}}}
  
 can be computed, which is non-zero. 
On the other hand, this is a non-invertible matrix: 

  
    
      
        
          C
        
        =
        
          
            (
            
              
                
                  2
                
                
                  4
                
              
              
                
                  2
                
                
                  4
                
              
            
            )
          
        
      
    
    {\\displaystyle \\mathbf {C} ={\\begin{pmatrix}2&4\\\\2&4\\end{pmatrix}}}
  

We can see the rank of this 2-by-2 matrix is 1, which is n − 1 ≠ n, so it is non-invertible. Additionally, we can compute that the determinant of 
  
    
      
        
          C
        
      
    
    {\\displaystyle \\mathbf {C} }
  
 is 0, which is a necessary and sufficient condition for a matrix to be non-invertible.


== Methods of matrix inversion ==


=== Gaussian elimination ===
Gaussian elimination is a useful and easy way to compute the inverse of a matrix. To compute a matrix inverse using this method, an augmented matrix is first created with the left side being the matrix to invert and the right side being the identity matrix.""",
    tier=4,
    domain="linear_algebra",
    source="Wikipedia, 'Invertible matrix'",
    source_url="https://en.wikipedia.org/wiki/Invertible_matrix",
))

register_atom(Atom(
    atom_type="theorem",
    name="eigenvalue",
    content="""In linear algebra, an eigenvector ( EYE-gən-) or characteristic vector is a (nonzero) vector that has its direction unchanged (or reversed) by a given linear transformation. More precisely, an eigenvector 
  
    
      
        
          v
        
      
    
    {\\displaystyle \\mathbf {v} }
  
 of a linear transformation 
  
    
      
        T
      
    
    {\\displaystyle T}
  
 is scaled by a constant factor 
  
    
      
        λ
      
    
    {\\displaystyle \\lambda }
  
 when the linear transformation is applied to it: 
  
    
      
        T
        
          v
        
        =
        λ
        
          v
        
      
    
    {\\displaystyle T\\mathbf {v} =\\lambda \\mathbf {v} }
  
. The corresponding eigenvalue, characteristic value, or characteristic root is the multiplying factor 
  
    
      
        λ
      
    
    {\\displaystyle \\lambda }
  
 (possibly a negative or complex number).
Geometrically, vectors are multi-dimensional quantities with magnitude and direction, often pictured as arrows. A linear transformation rotates, stretches, or shears the vectors upon which it acts. A linear transformation's eigenvectors are those vectors that are only stretched or shrunk, with neither rotation nor shear. The corresponding eigenvalue is the factor by which an eigenvector is stretched or shrunk. If the eigenvalue is negative, the eigenvector's direction is reversed.
The eigenvectors and eigenvalues of a linear transformation serve to characterize it, and so they play important roles in all areas where linear algebra is applied, from geology to quantum mechanics. In particular, it is often the case that a system is represented by a linear transformation whose outputs are fed as inputs to the same transformation (feedback). In such an application, the largest eigenvalue is of particular importance, because it governs the long-term behavior of the system after many applications of the linear transformation, and the associated eigenvector is the steady state of the system.


== Matrices ==
For an 
  
    
      
        n
        
          ×
        
        n
      
    
    {\\displaystyle n{\\times }n}
  
 matrix A and a nonzero 
  
    
      
        n
      
    
    {\\displaystyle n}
  
-vector 
  
    
      
        
          v
        
      
    
    {\\displaystyle \\mathbf {v} }
  
, if multiplying A by 
  
    
      
        
          v
        
      
    
    {\\displaystyle \\mathbf {v} }
  
 (denoted 
  
    
      
        A
        
          v
        
      
    
    {\\displaystyle A\\mathbf {v} }
  
) simply scales 
  
    
      
        
          v
        
      
    
    {\\displaystyle \\mathbf {v} }
  
 by a factor λ, where λ is a scalar, then 
  
    
      
        
          v
        
      
    
    {\\displaystyle \\mathbf {v} }
  
 is called an eigenvector of A, and λ is the corresponding eigenvalue. This relationship can be expressed as: 
  
    
      
        A
        
          v
        
        =
        λ
        
          v
        
      
    
    {\\displaystyle A\\mathbf {v} =\\lambda \\mathbf {v} }
  
.
Given an n-dimensional vector space and a choice of basis, there is a direct correspondence between linear transformations from the vector space into itself and n-by-n square matrices. Hence, in a finite-dimensional vector space, it is equivalent to define eigenvalues and eigenvectors using either the language of linear transformations, or the language of matrices.


== Overview ==
Eigenvalues and eigenvectors feature prominently in the analysis of linear transformations. The prefix eigen- is adopted from the German eigen (cognate with the English word own) for 'proper', 'characteristic', 'own'. Originally used to study principal axes of the rotational motion of rigid bodies, eigenvalues and eigenvectors have a wide range of applications, for example in stability analysis, vibration analysis, atomic orbitals, facial recognition, and matrix diagonalization.
In essence, an eigenvector v of a linear transformation T is a nonzero vector that, when T is applied to it, does not change direction. Applying T to the eigenvector only scales the eigenvector by the scalar value λ, called an eigenvalue. This condition can be written as the equation

  
    
      
        T
        (
        
          v
        
        )
        =
        λ
        
          v
        
        ,
      
    
    {\\displaystyle T(\\mathbf {v} )=\\lambda \\mathbf {v} ,}
  

referred to as the eigenvalue equation or eigenequation. In general, λ may be any scalar. For example, λ may be negative, in which case the eigenvector reverses direction as part of the scaling, or it may be zero or complex.

The example here, based on the Mona Lisa, provides a simple illustration. Each point on the painting can be represented as a vector pointing from the center of the painting to that point. The linear transformation in this example is called a shear mapping. Points in the top half are moved to the right, and points in the bottom half are moved to the left, proportional to how far they are from the horizontal axis that goes through the middle of the painting. The vectors pointing to each point in the original image are therefore tilted right or left, and made longer or shorter by the transformation. Points along the horizontal axis do not move at all when this transformation is applied. Therefore, any vector that points directly to the right or left with no vertical component is an eigenvector of this transformation, because the mapping does not change its direction. Moreover, these eigenvectors all have an eigenvalue equal to one, because the mapping does not change their length either.
Linear transformations can take many different forms, mapping vectors in a variety of vector spaces, so the eigenvectors can also take many forms. For example, the linear transformation could be a differential operator like 
  
    
      
        
          
            
              d
              
                d
                x
              
            
          
        
      
    
    {\\displaystyle {\\tfrac {d}{dx}}}
  
, in which case the eigenvectors are functions called eigenfunctions that are scaled by that differential operator, such as

  
    
      
        
          
            d
            
              d
              x
            
          
        
        
          e
          
            λ
            x
          
        
        =
        λ
        
          e
          
            λ
            x
          
        
        .
      
    
    {\\displaystyle {\\frac {d}{dx}}e^{\\lambda x}=\\lambda e^{\\lambda x}.}
  

Alternatively, the linear transformation could take the form of an n × n matrix, in which case the eigenvectors are n × 1 matrices. If the linear transformation is expressed in the form of an n × n matrix A, then the eigenvalue equation for a linear transformation above can be rewritten as the matrix multiplication

  
    
      
        A
        
          v
        
        =
        λ
        
          v
        
        ,
      
    
    {\\displaystyle A\\mathbf {v} =\\lambda \\mathbf {v} ,}
  

where the eigenvector v is an n × 1 matrix.""",
    tier=4,
    domain="linear_algebra",
    source="Wikipedia, 'Eigenvalues and eigenvectors'",
    source_url="https://en.wikipedia.org/wiki/Eigenvalues_and_eigenvectors",
))

register_atom(Atom(
    atom_type="algorithm",
    name="edit_distance",
    content="""In information theory, linguistics, and computer science, the Levenshtein distance is a string metric for measuring the difference between two sequences. The Levenshtein distance between two words is the minimum number of single-character edits (insertions, deletions or substitutions) required to change one word into the other. It is named after Soviet mathematician Vladimir Levenshtein, who defined the metric in 1965.
Levenshtein distance may also be referred to as edit distance, although that term may also denote a larger family of distance metrics. It is closely related to pairwise string alignments.


== Definition ==
The Levenshtein distance between two strings 
  
    
      
        a
        ,
        b
      
    
    {\\displaystyle a,b}
  
 (of length 
  
    
      
        
          |
        
        a
        
          |
        
      
    
    {\\displaystyle |a|}
  
 and 
  
    
      
        
          |
        
        b
        
          |
        
      
    
    {\\displaystyle |b|}
  
 respectively) is given by 
  
    
      
        lev
        ⁡
        (
        a
        ,
        b
        )
      
    
    {\\displaystyle \\operatorname {lev} (a,b)}
  
 where

  
    
      
        lev
        ⁡
        (
        a
        ,
        b
        )
        =
        
          
            {
            
              
                
                  
                    |
                  
                  a
                  
                    |
                  
                
                
                  
                     if 
                  
                  
                    |
                  
                  b
                  
                    |
                  
                  =
                  0
                  ,
                
              
              
                
                  
                    |
                  
                  b
                  
                    |
                  
                
                
                  
                     if 
                  
                  
                    |
                  
                  a
                  
                    |
                  
                  =
                  0
                  ,
                
              
              
                
                  lev
                  ⁡
                  
                    
                      (
                    
                  
                  tail
                  ⁡
                  (
                  a
                  )
                  ,
                  tail
                  ⁡
                  (
                  b
                  )
                  
                    
                      )
                    
                  
                
                
                  
                     if 
                  
                  head
                  ⁡
                  (
                  a
                  )
                  =
                  head
                  ⁡
                  (
                  b
                  )
                  ,
                
              
              
                
                  1
                  +
                  min
                  
                    
                      {
                      
                        
                          
                            lev
                            ⁡
                            
                              
                                (
                              
                            
                            tail
                            ⁡
                            (
                            a
                            )
                            ,
                            b
                            
                              
                                )
                              
                            
                          
                        
                        
                          
                            lev
                            ⁡
                            
                              
                                (
                              
                            
                            a
                            ,
                            tail
                            ⁡
                            (
                            b
                            )
                            
                              
                                )
                              
                            
                          
                        
                        
                          
                            lev
                            ⁡
                            
                              
                                (
                              
                            
                            tail
                            ⁡
                            (
                            a
                            )
                            ,
                            tail
                            ⁡
                            (
                            b
                            )
                            
                              
                                )
                              
                            
                          
                        
                      
                      
                    
                  
                
                
                  
                     otherwise
                  
                
              
            
            
          
        
      
    
    {\\displaystyle \\operatorname {lev} (a,b)={\\begin{cases}|a|&{\\text{ if }}|b|=0,\\\\|b|&{\\text{ if }}|a|=0,\\\\\\operatorname {lev} {\\big (}\\operatorname {tail} (a),\\operatorname {tail} (b){\\big )}&{\\text{ if }}\\operatorname {head} (a)=\\operatorname {head} (b),\\\\1+\\min {\\begin{cases}\\operatorname {lev} {\\big (}\\operatorname {tail} (a),b{\\big )}\\\\\\operatorname {lev} {\\big (}a,\\operatorname {tail} (b){\\big )}\\\\\\operatorname {lev} {\\big (}\\operatorname {tail} (a),\\operatorname {tail} (b){\\big )}\\\\\\end{cases}}&{\\text{ otherwise}}\\end{cases}}}
  

where the 
  
    
      
        tail
      
    
    {\\displaystyle \\operatorname {tail} }
  
 of some string 
  
    
      
        x
      
    
    {\\displaystyle x}
  
 is a string of all but the first character of 
  
    
      
        x
      
    
    {\\displaystyle x}
  
 (i.e. 
  
    
      
        tail
        ⁡
        (
        
          x
          
            0
          
        
        
          x
          
            1
          
        
        …
        
          x
          
            n
          
        
        )
        =
        
          x
          
            1
          
        
        
          x
          
            2
          
        
        …
        
          x
          
            n
          
        
      
    
    {\\displaystyle \\operatorname {tail} (x_{0}x_{1}\\dots x_{n})=x_{1}x_{2}\\dots x_{n}}
  
), and 
  
    
      
        head
        ⁡
        (
        x
        )
      
    
    {\\displaystyle \\operatorname {head} (x)}
  
 is the first character of 
  
    
      
        x
      
    
    {\\displaystyle x}
  
 (i.e. 
  
    
      
        head
        ⁡
        (
        
          x
          
            0
          
        
        
          x
          
            1
          
        
        …
        
          x
          
            n
          
        
        )
        =
        
          x
          
            0
          
        
      
    
    {\\displaystyle \\operatorname {head} (x_{0}x_{1}\\dots x_{n})=x_{0}}
  
).""",
    tier=4,
    domain="dynamic_programming",
    source="Wikipedia, 'Levenshtein distance'",
    source_url="https://en.wikipedia.org/wiki/Levenshtein_distance",
))

register_atom(Atom(
    atom_type="algorithm",
    name="coin_change",
    content="""The change-making problem addresses the question of finding the minimum number of coins (of certain denominations) that add up to a given amount of money. It is a special case of the integer knapsack problem, and has applications wider than just currency.
It is also the most common variation of the coin change problem, a general case of partition in which, given the available denominations of an infinite set of coins, the objective is to find out the number of possible ways of making a change for a specific amount of money, without considering the order of the coins.
It is weakly NP-hard, but may be solved optimally in pseudo-polynomial time by dynamic programming.


== Mathematical definition ==
Coin values can be modeled by a set of n distinct positive integer values (whole numbers), arranged in increasing order as w1 through wn. The problem is: given an amount W, also a positive integer, to find a set of non-negative (positive or zero) integers {x1, x2, ..., xn}, with each xj representing how often the coin with value wj is used, which minimize the total number of coins f(W)

  
    
      
        f
        (
        W
        )
        =
        
          ∑
          
            j
            =
            1
          
          
            n
          
        
        
          x
          
            j
          
        
      
    
    {\\displaystyle f(W)=\\sum _{j=1}^{n}x_{j}}
  

subject to

  
    
      
        
          ∑
          
            j
            =
            1
          
          
            n
          
        
        
          w
          
            j
          
        
        
          x
          
            j
          
        
        =
        W
        .
      
    
    {\\displaystyle \\sum _{j=1}^{n}w_{j}x_{j}=W.}
  


== Non-currency examples ==
An application of change-making problem can be found in computing the ways one can make a nine dart finish in a game of darts.
Another application is computing the possible atomic (or isotopic) composition of a given mass/charge peak in mass spectrometry.


== Methods of solving ==


=== Simple dynamic programming ===
A classic dynamic programming strategy works upward by finding the combinations of all smaller values that would sum to the current threshold. Thus, at each threshold, all previous thresholds are potentially considered to work upward to the goal amount W. For this reason, this dynamic programming approach requires a number of steps that is O(nW), where n is the number of types of coins.


==== Implementation ====
The following is a dynamic programming implementation (with Python 3) which uses a matrix to keep track of the optimal solutions to sub-problems, and returns the minimum number of coins, or "Infinity" if there is no way to make change with the coins given. A second matrix may be used to obtain the set of coins for the optimal solution.


=== Greedy method ===
For many real-world coin systems, such as those used in the US and many other countries, a greedy algorithm of picking the largest denomination of coin which is not greater than the remaining amount to be made will produce the optimal result. This is not the case for arbitrary coin systems or even some real world systems, though. For instance, if we consider the old (now withdrawn) Indian coin denominations of 5, 10, 20 and 25 paise, then to make 40 paise, the greedy algorithm would choose three coins (25, 10, 5) whereas the optimal solution is two coins (20, 20). Another example is attempting to make 40 US cents without nickels (denomination 25, 10, 1) with similar result — the greedy chooses seven coins (25, 10, and 5 × 1), but the optimal is four (4 × 10). A coin system is called "canonical" if the greedy algorithm always solves its change-making problem optimally. It is possible to test whether a coin system is canonical in polynomial time.


== Related problems ==
The "optimal denomination problem" is a problem for people who design entirely new currencies. It asks what denominations should be chosen for the coins in order to minimize the average cost of making change, that is, the average number of coins needed to make change. The version of this problem assumed that the people making change will use the minimum number of coins (from the denominations available). One variation of this problem assumes that the people making change will use the "greedy algorithm" for making change, even when that requires more than the minimum number of coins. Most current currencies use a 1-2-5 series, but some other set of denominations would require fewer denominations of coins or a smaller average number of coins to make change or both.


== See also ==
List of knapsack problems
Coin problem
The coin collector's problem


== References ==


== Further reading ==
M. Adamaszek, A. Niewiarowska (2010). "Combinatorics of the change-making problem". European Journal of Combinatorics. 31 (1): 47–63. arXiv:0801.0120. doi:10.1016/j.ejc.2009.05.002. S2CID 13527488.""",
    tier=4,
    domain="dynamic_programming",
    source="Wikipedia, 'Change-making problem'",
    source_url="https://en.wikipedia.org/wiki/Change-making_problem",
))

register_atom(Atom(
    atom_type="algorithm",
    name="shortest_path",
    content="""Dijkstra's algorithm (, DYKE-strəz) is an algorithm for finding the shortest paths between nodes in a weighted graph, which may represent, for example, a road network. It was conceived by computer scientist Edsger W. Dijkstra in 1956 and published three years later.
Dijkstra's algorithm finds the shortest path from a given source node to every other node. It can be used to find the shortest path to a specific destination node, by terminating the algorithm after determining the shortest path to that node. For example, if the nodes of the graph represent cities, and the costs of edges represent the distances between pairs of cities connected by a direct road, then Dijkstra's algorithm can be used to find the shortest route between one city and all other cities. A common application of shortest path algorithms is network routing protocols, most notably IS-IS (Intermediate System to Intermediate System) and OSPF (Open Shortest Path First). It is also employed as a subroutine in algorithms such as Johnson's algorithm.
The algorithm uses a min-priority queue data structure for selecting the shortest paths known so far. Before more advanced priority queue structures were discovered, Dijkstra's original algorithm ran in 
  
    
      
        Θ
        (
        
          |
        
        V
        
          
            |
          
          
            2
          
        
        )
      
    
    {\\displaystyle \\Theta (|V|^{2})}
  
 time, where 
  
    
      
        
          |
        
        V
        
          |
        
      
    
    {\\displaystyle |V|}
  
 is the number of nodes. Fredman & Tarjan 1984 proposed a Fibonacci heap priority queue to optimize the running time complexity to 
  
    
      
        Θ
        (
        
          |
        
        E
        
          |
        
        +
        
          |
        
        V
        
          |
        
        log
        ⁡
        
          |
        
        V
        
          |
        
        )
      
    
    {\\displaystyle \\Theta (|E|+|V|\\log |V|)}
  
, where 
  
    
      
        
          |
        
        E
        
          |
        
      
    
    {\\displaystyle |E|}
  
 is the number of edges. This is asymptotically the fastest known single-source shortest-path algorithm for arbitrary directed graphs with unbounded non-negative weights. However, specialized cases (such as bounded/integer weights, directed acyclic graphs etc.) can be improved further. If preprocessing is allowed, algorithms such as contraction hierarchies can be up to seven orders of magnitude faster.
Dijkstra's algorithm is commonly used on graphs where the edge weights are positive integers or real numbers. It can be generalized to any graph where the edge weights are partially ordered, provided the subsequent labels (a subsequent label is produced when traversing an edge) are monotonically non-decreasing.
In many fields, particularly artificial intelligence, Dijkstra's algorithm or a variant offers a uniform cost search and is formulated as an instance of the more general idea of best-first search.


== History ==
What is the shortest way to travel from Rotterdam to Groningen, in general: from given city to given city. It is the algorithm for the shortest path, which I designed in about twenty minutes. One morning I was shopping in Amsterdam with my young fiancée, and tired, we sat down on the café terrace to drink a cup of coffee and I was just thinking about whether I could do this, and I then designed the algorithm for the shortest path. As I said, it was a twenty-minute invention. In fact, it was published in '59, three years later. The publication is still readable, it is, in fact, quite nice. One of the reasons that it is so nice was that I designed it without pencil and paper. I learned later that one of the advantages of designing without pencil and paper is that you are almost forced to avoid all avoidable complexities. Eventually, that algorithm became to my great amazement, one of the cornerstones of my fame.
Dijkstra thought about the shortest path problem while working as a programmer at the Mathematical Center in Amsterdam in 1956. He wanted to demonstrate the capabilities of the new ARMAC computer. His objective was to choose a problem and a computer solution that non-computing people could understand. He designed the shortest path algorithm and later implemented it for ARMAC for a slightly simplified transportation map of 64 cities in the Netherlands (he limited it to 64, so that 6 bits would be sufficient to encode the city number). A year later, he came across another problem advanced by hardware engineers working on the institute's next computer: minimize the amount of wire needed to connect the pins on the machine's back panel. As a solution, he re-discovered Prim's minimal spanning tree algorithm (known earlier to Jarník, and also rediscovered by Prim). Dijkstra published the algorithm in 1959, two years after Prim and 29 years after Jarník.


== Algorithm ==

The algorithm requires a starting node, and computes the shortest distance from that starting node to each other node. Dijkstra's algorithm starts with infinite distances and tries to improve them step by step:

Create a set of all unvisited nodes: the unvisited set.
Assign to every node a distance from start value: for the starting node, it is zero, and for all other nodes, it is infinity, since initially no path is known to these nodes. During execution, the distance of a node N is the length of the shortest path discovered so far between the starting node and N.
From the unvisited set, select the current node to be the one with the smallest (finite) distance; initially, this is the starting node (distance zero). If the unvisited set is empty, or contains only nodes with infinite distance (which are unreachable), then the algorithm terminates by skipping to step 6. If the only concern is the path to a target node, the algorithm terminates once the current node is the target node. Otherwise, the algorithm continues.
For the current node, consider all of its unvisited neighbors and update their distances through the current node; compare the newly calculated distance to the one currently assigned to the neighbor and assign the smaller one to it. For example, if the current node A is marked with a distance of 6, and the edge connecting it with its neighbor B has length 2, then the distance to B through A is 6 + 2 = 8. If B was previously marked with a distance greater than 8, then update it to 8 (the path to B through A is shorter). Otherwise, keep its current distance (the path to B through A is not the shortest).
After considering all of the current node's unvisited neighbors, the current node is removed from the unvisited set. Thus a visited node is never rechecked, which is correct because the distance recorded on the current node is minimal (as ensured in step 3), and thus final. Repeat from step 3.
Once the loop exits (steps 3–5), every visited node contains its shortest distance from the starting node.


== Description ==

The shortest path between two intersections on a city map can be found by this algorithm using pencil and paper. Every intersection is listed on a separate line: one is the starting point and is labeled (given a distance of) 0. Every other intersection is initially labeled with a distance of infinity. This is done to note that no path to these intersections has yet been established. At each iteration one intersection becomes the current intersection. For the first iteration, this is the starting point.
From the current intersection, the distance to every neighbor (directly-connected) intersection is assessed by summing the label (value) of the current intersection and the distance to the neighbor and then relabeling the neighbor with the lesser of that sum and the neighbor's existing label.""",
    tier=4,
    domain="graph_theory",
    source="Wikipedia, 'Dijkstra's algorithm'",
    source_url="https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm",
))

register_atom(Atom(
    atom_type="theorem",
    name="derivative_eval",
    content="""In mathematics, the derivative is a fundamental tool that quantifies the sensitivity to change of a function's output with respect to its input. The derivative of a function of a single variable at a chosen input value, when it exists, is the slope of the tangent line to the graph of the function at that point. The tangent line is the best linear approximation of the function near that input value. The derivative is often described as the instantaneous rate of change, the ratio of the instantaneous change in the dependent variable to that of the independent variable. The process of finding a derivative is called differentiation.
There are multiple different notations for differentiation. Leibniz notation, named after Gottfried Wilhelm Leibniz, is represented as the ratio of two differentials, whereas prime notation is written by adding a prime mark. Higher order notations represent repeated differentiation, and they are usually denoted in Leibniz notation by adding superscripts to the differentials, and in prime notation by adding additional prime marks. Higher order derivatives are used in physics; for example, the first derivative  with respect to time of the position of a moving object is its velocity, and the second derivative is its acceleration.
Derivatives can be generalized to functions of several real variables. In this case, the derivative is reinterpreted as a linear transformation whose graph is (after an appropriate translation) the best linear approximation to the graph of the original function. The Jacobian matrix is the matrix that represents this linear transformation with respect to the basis given by the choice of independent and dependent variables.  It can be calculated in terms of the partial derivatives with respect to the independent variables.  For a real-valued function of several variables, the Jacobian matrix reduces to the gradient vector.


== Definition ==


=== As a limit ===
A function of a real variable 
  
    
      
        f
        (
        x
        )
      
    
    {\\displaystyle f(x)}
  
 is differentiable at a point 
  
    
      
        a
      
    
    {\\displaystyle a}
  
 of its domain, if its domain contains an open interval containing ⁠
  
    
      
        a
      
    
    {\\displaystyle a}
  
⁠, and the limit

  
    
      
        L
        =
        
          lim
          
            h
            →
            0
          
        
        
          
            
              f
              (
              a
              +
              h
              )
              −
              f
              (
              a
              )
            
            h
          
        
      
    
    {\\displaystyle L=\\lim _{h\\to 0}{\\frac {f(a+h)-f(a)}{h}}}
  

exists.  This means that, for every positive real number ⁠
  
    
      
        ε
      
    
    {\\displaystyle \\varepsilon }
  
⁠, there exists a positive real number 
  
    
      
        δ
      
    
    {\\displaystyle \\delta }
  
 such that, for every 
  
    
      
        h
      
    
    {\\displaystyle h}
  
 such that 
  
    
      
        
          |
        
        h
        
          |
        
        <
        δ
      
    
    {\\displaystyle |h|<\\delta }
  
 and 
  
    
      
        h
        ≠
        0
      
    
    {\\displaystyle h\\neq 0}
  
 then 
  
    
      
        f
        (
        a
        +
        h
        )
      
    
    {\\displaystyle f(a+h)}
  
 is defined, and 

  
    
      
        
          |
          
            L
            −
            
              
                
                  f
                  (
                  a
                  +
                  h
                  )
                  −
                  f
                  (
                  a
                  )
                
                h
              
            
          
          |
        
        <
        ε
        ,
      
    
    {\\displaystyle \\left|L-{\\frac {f(a+h)-f(a)}{h}}\\right|<\\varepsilon ,}
  

where the vertical bars denote the absolute value. This is an example of the (ε, δ)-definition of limit.
If the function 
  
    
      
        f
      
    
    {\\displaystyle f}
  
 is differentiable at ⁠
  
    
      
        a
      
    
    {\\displaystyle a}
  
⁠, that is if the limit 
  
    
      
        L
      
    
    {\\displaystyle L}
  
 exists, then this limit is called the derivative of 
  
    
      
        f
      
    
    {\\displaystyle f}
  
 at ⁠
  
    
      
        a
      
    
    {\\displaystyle a}
  
⁠. Multiple notations for the derivative exist. The derivative of 
  
    
      
        f
      
    
    {\\displaystyle f}
  
 at 
  
    
      
        a
      
    
    {\\displaystyle a}
  
 can be denoted ⁠
  
    
      
        
          f
          ′
        
        (
        a
        )
      
    
    {\\displaystyle f'(a)}
  
⁠, read as "⁠
  
    
      
        f
      
    
    {\\displaystyle f}
  
⁠ prime of ⁠
  
    
      
        a
      
    
    {\\displaystyle a}
  
⁠"; or it can be denoted ⁠
  
    
      
        
          
            
              
                d
                f
              
              
                d
                x
              
            
          
          (
          a
          )
        
      
    
    {\\displaystyle \\textstyle {\\frac {df}{dx}}(a)}
  
⁠, read as "the derivative of 
  
    
      
        f
      
    
    {\\displaystyle f}
  
 with respect to 
  
    
      
        x
      
    
    {\\displaystyle x}
  
 at ⁠
  
    
      
        a
      
    
    {\\displaystyle a}
  
⁠" or "⁠
  
    
      
        d
        f
      
    
    {\\displaystyle df}
  
⁠ by (or over) 
  
    
      
        d
        x
      
    
    {\\displaystyle dx}
  
 at ⁠
  
    
      
        a
      
    
    {\\displaystyle a}
  
⁠". See § Notation below. If 
  
    
      
        f
      
    
    {\\displaystyle f}
  
 is a function that has a derivative at every point in its domain, then a function can be defined by mapping every point 
  
    
      
        x
      
    
    {\\displaystyle x}
  
 to the value of the derivative of 
  
    
      
        f
      
    
    {\\displaystyle f}
  
 at ⁠
  
    
      
        x
      
    
    {\\displaystyle x}
  
⁠. This function is written 
  
    
      
        
          f
          ′
        
      
    
    {\\displaystyle f'}
  
 and is called the derivative function or the derivative of ⁠
  
    
      
        f
      
    
    {\\displaystyle f}
  
⁠. The function 
  
    
      
        f
      
    
    {\\displaystyle f}
  
 sometimes has a derivative at most, but not all, points of its domain. The function whose value at 
  
    
      
        a
      
    
    {\\displaystyle a}
  
 equals 
  
    
      
        
          f
          ′
        
        (
        a
        )
      
    
    {\\displaystyle f'(a)}
  
 whenever 
  
    
      
        
          f
          ′
        
        (
        a
        )
      
    
    {\\displaystyle f'(a)}
  
 is defined and elsewhere is undefined is also called the derivative of ⁠
  
    
      
        f
      
    
    {\\displaystyle f}
  
⁠. It is still a function, but its domain may be smaller than the domain of ⁠
  
    
      
        f
      
    
    {\\displaystyle f}
  
⁠.
For example, let 
  
    
      
        f
      
    
    {\\displaystyle f}
  
 be the squaring function: ⁠
  
    
      
        f
        (
        x
        )
        =
        
          x
          
            2
          
        
      
    
    {\\displaystyle f(x)=x^{2}}
  
⁠.""",
    tier=4,
    domain="calculus",
    source="Wikipedia, 'Derivative'",
    source_url="https://en.wikipedia.org/wiki/Derivative",
))

register_atom(Atom(
    atom_type="algorithm",
    name="number_base_arithmetic",
    content="""Positional notation, also known as place-value notation, is the property of a numeral system that the value represented by each symbol in a written numeral depends not only on its appearance but also on its position. Each symbol fits in a specific place or position, representing a power of a fixed base. The most common numeral system used today, the Hindu–Arabic numeral system, is a positional system in base ten; each of ten numerical digits is a distinct symbol representing one the numbers zero through nine, and in the context of the full numeral, each symbol's value is the digit multiplied by a power of ten.
Most early numeral systems, such as Roman numerals, are essentially based on the additive principle: each symbol type represents one fixed value, and the value of a numeral is the sum of the values of the separate symbols. For example, the Roman numeral CCXXVIII has two copies of the symbol C meaning 100, two copies of X meaning 10, one V meaning 5, and three copies of I meaning 1, so overall represents the number 100 + 100 + 10 + 10 + 5 + 1 + 1 + 1 = 228; by comparison, the equivalent Hindu–Arabic numeral, 228, consists of the symbol 2 representing 2 × 100, another symbol 2 representing 2 × 10, and finally an 8 representing 8 × 1.
The Babylonian numeral system, base 60, was the first positional system to be developed, and its influence is present today in the way time and angles are counted in tallies related to 60, such as 60 minutes in an hour and 360 degrees in a circle. The Inca used knots tied in a decimal positional system to store numbers and other values in quipu cords.
The binary numeral system (base two) is used in almost all computers and electronic devices because it is easier to implement efficiently in electronic circuits.
Systems with negative base, complex base or negative digits have been described. Most of them do not require a minus sign for designating negative numbers.
The use of a radix point (decimal point in base ten), extends to include fractions and allows the representation of any real number with arbitrary accuracy. With positional notation, arithmetical computations are much simpler than with any older numeral system; this led to the rapid spread of the notation when it was introduced in western Europe.


== History ==

Today, the base-10 (decimal) system, which is presumably motivated by counting with the ten fingers, is ubiquitous. Other bases have been used in the past, and some continue to be used today. For example, the Babylonian numeral system, credited as the first positional numeral system, was base-60. However, it lacked a real zero. Initially inferred only from context, later, by about 700 BC, zero came to be indicated by a "space" or a "punctuation symbol" (such as two slanted wedges) between numerals. It was a placeholder rather than a true zero because it was not used alone or at the end of a number. Numbers like 2 and 120 (2×60) looked the same because the larger number lacked a final placeholder. Only context could differentiate them.
The polymath Archimedes (ca. 287–212 BC) invented a decimal positional system based on 108 in his Sand Reckoner; 19th century German mathematician Carl Gauss lamented how science might have progressed had Archimedes only made the leap to something akin to the modern decimal system. Hellenistic and Roman astronomers used a base-60 system based on the Babylonian model (see Greek numerals § Zero).
Before positional notation became standard, simple additive systems (sign-value notation) such as Roman numerals or Chinese numerals were used, and accountants in the past used the abacus or stone counters to do arithmetic until the introduction of positional notation.

Counting rods and most abacuses have been used to represent numbers in a positional numeral system. With counting rods or abacus to perform arithmetic operations, the writing of the starting, intermediate and final values of a calculation could easily be done with a simple additive system in each position or column. This approach required no memorization of tables (as does positional notation) and could produce practical results quickly.
The oldest extant positional notation system is either that of Chinese rod numerals, used from at least the early 8th century, or perhaps Khmer numerals, showing possible usages of positional-numbers in the 7th century. Khmer numerals and other Indian numerals originate with the Brahmi numerals of about the 3rd century BC, which symbols were, at the time, not used positionally. Medieval Indian numerals are positional, as are the derived Arabic numerals, recorded from the 10th century.
After the French Revolution (1789–1799), the new French government promoted the extension of the decimal system. Some of those pro-decimal efforts—such as decimal time and the decimal calendar—were unsuccessful. Other French pro-decimal efforts—currency decimalisation and the metrication of weights and measures—spread widely out of France to almost the whole world.


=== History of positional fractions ===

Decimal fractions were first developed and used by the Chinese in the form of rod calculus in the 1st century BC, and then spread to the rest of the world. J. Lennart Berggren notes that positional decimal fractions were being used in Damascus by mathematician Abu'l-Hasan al-Uqlidisi in the mid 10th century. The Jewish mathematician Immanuel Bonfils used decimal fractions around 1350, but did not develop any notation to represent them. The Persian mathematician Jamshīd al-Kāshī similarly adopted their use in the 15th century. Al Khwarizmi introduced fractions to Islamic countries in the early 9th century; his fraction presentation was similar to the traditional Chinese mathematical fractions from Sunzi Suanjing. This form of fraction with numerator on top and denominator at bottom without a horizontal bar was also used by 10th century Abu'l-Hasan al-Uqlidisi and 15th century Jamshīd al-Kāshī's work "Arithmetic Key".

The adoption of the decimal representation of numbers less than one, a fraction, is often credited to Simon Stevin through his textbook De Thiende; but both Stevin and E. J. Dijksterhuis indicate that Regiomontanus contributed to the European adoption of general decimals:

European mathematicians, when taking over from the Hindus, via the Arabs, the idea of positional value for integers, neglected to extend this idea to fractions. For some centuries they confined themselves to using common and sexagesimal fractions ... This half-heartedness has never been completely overcome, and sexagesimal fractions still form the basis of our trigonometry, astronomy and measurement of time.
... Mathematicians sought to avoid fractions by taking the radius R equal to a number of units of length of the form 10n and then assuming for n so great an integral value that all occurring quantities could be expressed with sufficient accuracy by integers.

The first to apply this method was the German astronomer Regiomontanus. To the extent that he expressed goniometrical line-segments in a unit R/10n, Regiomontanus may be called an anticipator of the doctrine of decimal positional fractions.
In the estimation of Dijksterhuis, "after the publication of De Thiende only a small advance was required to establish the complete system of decimal positional fractions, and this step was taken promptly by a number of writers ... next to Stevin the most important figure in this development was Regiomontanus." Dijksterhuis noted that [Stevin] "gives full credit to Regiomontanus for his prior contribution, saying that the trigonometric tables of the German astronomer actually contain the whole theory of 'numbers of the tenth progress'."


== Mathematics ==


=== Base of the numeral system ===
In mathematical numeral systems the radix r is usually the number of unique digits, including zero, that a positional numeral system uses to represent numbers.""",
    tier=4,
    domain="number_theory",
    source="Wikipedia, 'Positional notation'",
    source_url="https://en.wikipedia.org/wiki/Positional_notation",
))

register_atom(Atom(
    atom_type="theorem",
    name="limit",
    content="""In mathematics, a limit is the value that a function (or sequence) approaches as the argument (or index) approaches some value. Limits of functions are essential to calculus and mathematical analysis, and are used to define continuity, derivatives, and integrals.
The concept of a limit of a sequence is further generalized to the concept of a limit of a topological net, and is closely related to limit and direct limit in category theory.
The limit inferior and limit superior provide generalizations of the concept of a limit which are particularly relevant when the limit at a point may not exist.


== Notation ==
In formulas, a limit of a function is usually written as

  
    
      
        
          lim
          
            x
            →
            c
          
        
        f
        (
        x
        )
        =
        L
        ,
      
    
    {\\displaystyle \\lim _{x\\to c}f(x)=L,}
  

and is read as "the limit of 
  
    
      
        f
      
    
    {\\displaystyle f}
  
 of 
  
    
      
        x
      
    
    {\\displaystyle x}
  
 as 
  
    
      
        x
      
    
    {\\displaystyle x}
  
 approaches 
  
    
      
        c
      
    
    {\\displaystyle c}
  
 equals 
  
    
      
        L
      
    
    {\\displaystyle L}
  
". This means that the value of the function 
  
    
      
        f
      
    
    {\\displaystyle f}
  
 can be made arbitrarily close to 
  
    
      
        L
      
    
    {\\displaystyle L}
  
, by choosing 
  
    
      
        x
      
    
    {\\displaystyle x}
  
 sufficiently close to 
  
    
      
        c
      
    
    {\\displaystyle c}
  
. Alternatively, the fact that a function 
  
    
      
        f
      
    
    {\\displaystyle f}
  
 approaches the limit 
  
    
      
        L
      
    
    {\\displaystyle L}
  
 as 
  
    
      
        x
      
    
    {\\displaystyle x}
  
 approaches 
  
    
      
        c
      
    
    {\\displaystyle c}
  
 is sometimes denoted by a right arrow (→ or 
  
    
      
        →
      
    
    {\\displaystyle \\rightarrow }
  
), as in

  
    
      
        f
        (
        x
        )
        →
        L
        
           as 
        
        x
        →
        c
        ,
      
    
    {\\displaystyle f(x)\\to L{\\text{ as }}x\\to c,}
  

or in

  
    
      
        f
        (
        x
        )
        
          
            →
            
              
                x
                →
                c
              
            
            
          
        
        L
        ,
      
    
    {\\displaystyle f(x){\\xrightarrow[{x\\to c}]{}}L,}
  

which reads "
  
    
      
        f
      
    
    {\\displaystyle f}
  
 of 
  
    
      
        x
      
    
    {\\displaystyle x}
  
 tends to 
  
    
      
        L
      
    
    {\\displaystyle L}
  
 as 
  
    
      
        x
      
    
    {\\displaystyle x}
  
 tends to 
  
    
      
        c
      
    
    {\\displaystyle c}
  
".


== History ==
According to Hankel (1871), the modern concept of limit originates from Proposition X.1 of Euclid's Elements, which forms the basis of the Method of exhaustion found in Euclid and Archimedes: "Two unequal magnitudes being set out, if from the greater there is subtracted a magnitude greater than its half, and from that which is left a magnitude greater than its half, and if this process is repeated continually, then there will be left some magnitude less than the lesser magnitude set out."
Grégoire de Saint-Vincent gave the first definition of limit (terminus) of a geometric series in his work Opus Geometricum (1647): "The terminus of a progression is the end of the series, which none progression can reach, even not if she is continued in infinity, but which she can approach nearer than a given segment." 
In the Scholium to Principia in 1687, Isaac Newton had a clear definition of a limit, stating that "Those ultimate ratios ... are not actually ratios of ultimate quantities, but limits ... which they can approach so closely that their difference is less than any given quantity". Bruce Pourciau further argues that, in addition to Newton actually having a more sophisticated understanding of limits than he is generally credited with, he also provided the first epsilon argument.
The modern definition of a limit goes back to Bernard Bolzano who, in 1817, developed the basics of the epsilon-delta technique to define continuous functions. However, his work remained unknown to other mathematicians until thirty years after his death.
Augustin-Louis Cauchy in 1821, followed by Karl Weierstrass, formalized the definition of the limit of a function which became known as the (ε, δ)-definition of limit.
The modern notation of placing the arrow below the limit symbol was invented by John Gaston Leathem in 1905 and popularized by G. H. Hardy's 1908 textbook A Course of Pure Mathematics.


== Types of limits ==


=== In sequences ===


==== Real numbers ====
The expression 0.999... should be interpreted as the limit of the sequence 0.9, 0.99, 0.999, ... and so on. This sequence can be rigorously shown to have the limit 1, and therefore this expression is meaningfully interpreted as having the value 1.
Formally, suppose a1, a2, ... is a sequence of real numbers. When the limit of the sequence exists, the real number L is the limit of this sequence if and only if for every real number ε > 0, there exists a natural number N such that for all n > N, we have |an − L| < ε.
The common notation

  
    
      
        
          lim
          
            n
            →
            ∞
          
        
        
          a
          
            n
          
        
        =
        L
      
    
    {\\displaystyle \\lim _{n\\to \\infty }a_{n}=L}
  

is read as:

 or 
The formal definition intuitively means that eventually, all elements of the sequence get arbitrarily close to the limit, since the absolute value |an − L| is the distance between an and L. 
Not every sequence has a limit. A sequence with a limit is called convergent; otherwise it is called divergent. One can show that a convergent sequence has only one limit.
The limit of a sequence and the limit of a function are closely related. On one hand, the limit as n approaches infinity of a sequence {an} is simply the limit at infinity of a function a(n)—defined on the natural numbers {n}. On the other hand, if X is the domain of a function f(x) and if the limit as n approaches infinity of f(xn) is L for every arbitrary sequence of points {xn} in X − x0 which converges to x0, then the limit of the function f(x) as x approaches x0 is equal to L. One such sequence would be {x0 + 1/n}.


==== Infinity as a limit ====
There is also a notion of having a limit "tend to infinity", rather than to a finite value 
  
    
      
        L
      
    
    {\\displaystyle L}
  
. A sequence 
  
    
      
        {
        
          a
          
            n
          
        
        }
      
    
    {\\displaystyle \\{a_{n}\\}}
  
 is said to "tend to infinity" if, for each real number 
  
    
      
        M
        >
        0
      
    
    {\\displaystyle M>0}
  
, known as the bound, there exists an integer 
  
    
      
        N
      
    
    {\\displaystyle N}
  
 such that for each 
  
    
      
        n
        >
        N
      
    
    {\\displaystyle n>N}
  
, 

  
    
      
        
          a
          
            n
          
        
        >
        M
        .
      
    
    {\\displaystyle a_{n}>M.}
  

That is, for every possible bound, the sequence eventually exceeds the bound.""",
    tier=5,
    domain="calculus",
    source="Wikipedia, 'Limit (mathematics)'",
    source_url="https://en.wikipedia.org/wiki/Limit_%28mathematics%29",
))

register_atom(Atom(
    atom_type="identity",
    name="complex_division",
    content="""In mathematics, a complex number is an element of a number system that extends the real numbers with a specific element denoted i, called the imaginary unit and satisfying the equation 
  
    
      
        
          i
          
            2
          
        
        =
        −
        1
      
    
    {\\displaystyle i^{2}=-1}
  
; because no real number satisfies the above equation, i was called an imaginary number by René Descartes. Every complex number can be expressed in the form 
  
    
      
        a
        +
        b
        i
      
    
    {\\displaystyle a+bi}
  
, where a and b are real numbers, a is called the real part, and b is called the imaginary part. The set of complex numbers is denoted by either of the symbols 
  
    
      
        
          C
        
      
    
    {\\displaystyle \\mathbb {C} }
  
 or C. Despite the historical nomenclature, "imaginary" complex numbers have a mathematical existence as firm as that of the real numbers, and they are fundamental tools in the scientific description of the natural world.
Complex numbers allow solutions to all polynomial equations, even those that have no solutions in real numbers. More precisely, the fundamental theorem of algebra asserts that every non-constant polynomial equation with real or complex coefficients has a solution which is a complex number. For example, the equation

  
    
      
        (
        x
        +
        1
        
          )
          
            2
          
        
        =
        −
        9
      
    
    {\\displaystyle (x+1)^{2}=-9}
  

has no real solution, because the square of a real number cannot be negative, but has the two nonreal complex solutions 
  
    
      
        x
        =
        −
        1
        +
        3
        i
      
    
    {\\displaystyle x=-1+3i}
  
 and 
  
    
      
        x
        =
        −
        1
        −
        3
        i
      
    
    {\\displaystyle x=-1-3i}
  
.
Addition, subtraction and multiplication of complex numbers are defined, taking advantage of the rule 
  
    
      
        
          i
          
            2
          
        
        =
        −
        1
      
    
    {\\displaystyle i^{2}=-1}
  
, along with the associative, commutative, and distributive laws. Every nonzero complex number has a multiplicative inverse, allowing division by complex numbers other than zero. This makes the complex numbers a field with the real numbers as a subfield. Because of these properties, ⁠
  
    
      
        a
        +
        b
        i
        =
        a
        +
        i
        b
      
    
    {\\displaystyle a+bi=a+ib}
  
⁠, and which form is written depends upon convention and style considerations.
The complex numbers also form a real vector space of dimension two, with 
  
    
      
        {
        1
        ,
        i
        }
      
    
    {\\displaystyle \\{1,i\\}}
  
 as a standard basis. This standard basis makes the complex numbers a Cartesian plane, called the complex plane. This allows a geometric interpretation of the complex numbers and their operations, and conversely some geometric objects and operations can be expressed in terms of complex numbers. For example, the real numbers form the real line, which is pictured as the horizontal axis of the complex plane, while real multiples of 
  
    
      
        i
      
    
    {\\displaystyle i}
  
 are the vertical axis. A complex number can also be defined by its geometric polar coordinates: the radius is called the absolute value of the complex number, while the angle from the positive real axis is called the argument of the complex number. The complex numbers of absolute value one form the unit circle. Adding a fixed complex number to all complex numbers defines a translation in the complex plane, and multiplying by a fixed complex number is a similarity centered at the origin (dilating by the absolute value, and rotating by the argument). The operation of complex conjugation is the reflection symmetry with respect to the real axis. 
The complex numbers form a rich structure that is simultaneously an algebraically closed field, a commutative algebra over the reals, and a Euclidean vector space of dimension two. 


== Definition and basic operations ==

A complex number is an expression of the form a + bi, where a and b are real numbers, and i is an abstract symbol, the so-called imaginary unit, whose meaning will be explained further below. For example, 2 + 3i is a complex number.
For a complex number a + bi, the real number a is called its real part, and the real number b (not the complex number bi) is its imaginary part. The real part of a complex number z is denoted Re(z), 
  
    
      
        
          
            R
            e
          
        
        (
        z
        )
      
    
    {\\displaystyle {\\mathcal {Re}}(z)}
  
, or 
  
    
      
        
          
            R
          
        
        (
        z
        )
      
    
    {\\displaystyle {\\mathfrak {R}}(z)}
  
; the imaginary part is Im(z), 
  
    
      
        
          
            I
            m
          
        
        (
        z
        )
      
    
    {\\displaystyle {\\mathcal {Im}}(z)}
  
, or 
  
    
      
        
          
            I
          
        
        (
        z
        )
      
    
    {\\displaystyle {\\mathfrak {I}}(z)}
  
: for example, 
  
    
      
        Re
        ⁡
        (
        2
        +
        3
        i
        )
        =
        2
      
    
    {\\textstyle \\operatorname {Re} (2+3i)=2}
  
, 
  
    
      
        Im
        ⁡
        (
        2
        +
        3
        i
        )
        =
        3
      
    
    {\\displaystyle \\operatorname {Im} (2+3i)=3}
  
.
A complex number z can be identified with the ordered pair of real numbers 
  
    
      
        (
        ℜ
        (
        z
        )
        ,
        ℑ
        (
        z
        )
        )
      
    
    {\\displaystyle (\\Re (z),\\Im (z))}
  
, which may be interpreted as coordinates of a point in a Euclidean plane with standard coordinates, which is then called the complex plane or Argand diagram. The horizontal axis is generally used to display the real part, with increasing values to the right, and the imaginary part marks the vertical axis, with increasing values upwards. 
A real number a can be regarded as a complex number a + 0i, whose imaginary part is 0. A purely imaginary number bi is a complex number 0 + bi, whose real part is zero. It is common to write a + 0i = a, 0 + bi = bi, and a + (−b)i = a − bi; for example, 3 + (−4)i = 3 − 4i.
The set of all complex numbers is denoted by 
  
    
      
        
          C
        
      
    
    {\\displaystyle \\mathbb {C} }
  
 (blackboard bold) or C (upright bold).
In some disciplines such as electromagnetism and electrical engineering, j is used instead of i, as i frequently represents electric current, and complex numbers are written as a + bj or a + jb.


=== Addition and subtraction ===

Two complex numbers 
  
    
      
        a
        =
        x
        +
        y
        i
      
    
    {\\displaystyle a=x+yi}
  
 and 
  
    
      
        b
        =
        u
        +
        v
        i
      
    
    {\\displaystyle b=u+vi}
  
 are added by separately adding their real and imaginary parts.""",
    tier=5,
    domain="complex_analysis",
    source="Wikipedia, 'Complex number'",
    source_url="https://en.wikipedia.org/wiki/Complex_number",
))

register_atom(Atom(
    atom_type="algorithm",
    name="topo_sort",
    content="""In computer science, a topological sort or topological ordering of a directed graph is a linear ordering of its vertices such that for every directed edge (u,v) from vertex u to vertex v, u comes before v in the ordering. For instance, the vertices of the graph may represent tasks to be performed, and the edges may represent constraints that one task must be performed before another; in this application, a topological ordering is just a valid sequence for the tasks. 
Precisely, a topological sort is a graph traversal in which each node v is visited only after all its dependencies are visited. A topological ordering is possible if and only if the graph has no directed cycles, that is, if it is a directed acyclic graph (DAG). Any DAG has at least one topological ordering, and there are  linear time algorithms for constructing it. Topological sorting has many applications, especially in ranking problems such as feedback arc set. Topological sorting is also possible when the DAG has disconnected components.


== Examples ==

The canonical application of topological sorting is in scheduling a sequence of jobs or tasks based on their dependencies. The jobs are represented by vertices, and there is an edge from x to y if job x must be completed before job y can be started (for example, when washing clothes, the washing machine must finish before we put the clothes in the dryer). Then, a topological sort gives an order in which to perform the jobs.  A closely related application of topological sorting algorithms was first studied in the early 1960s in the context of the PERT technique for scheduling in project management. In this application, the vertices of a graph represent the milestones of a project, and the edges represent tasks that must be performed between one milestone and another. Topological sorting forms the basis of linear-time algorithms for finding the critical path of the project, a sequence of milestones and tasks that controls the length of the overall project schedule.
In computer science, applications of this type arise in instruction scheduling, ordering of formula cell evaluation when recomputing formula values in spreadsheets, logic synthesis, determining the order of compilation tasks to perform in makefiles, data serialization, and resolving symbol dependencies in linkers. It is also used to decide in which order to load tables with foreign keys in databases.


== Algorithms ==
The usual algorithms for topological sorting have running time linear in the number of nodes plus the number of edges, asymptotically, 
  
    
      
        O
        (
        
          |
          
            V
          
          |
        
        +
        
          |
          
            E
          
          |
        
        )
        .
      
    
    {\\displaystyle O(\\left|{V}\\right|+\\left|{E}\\right|).}
  


=== Kahn's algorithm ===

One of these algorithms, first described by Kahn (1962), works by choosing vertices in the same order as the eventual topological sort. First, find a list of "start nodes" that have no incoming edges and insert them into a set S; at least one such node must exist in a non-empty (finite) acyclic graph. Then:

L ← Empty list that will contain the sorted elements
S ← Set of all nodes with no incoming edge

while S is not empty do
    remove a node n from S
    add n to L
    for each node m with an edge e from n to m do
        remove edge e from the graph
        if m has no other incoming edges then
            insert m into S

if graph has edges then
    return error   (graph has at least one cycle)
else 
    return L   (a topologically sorted order)

If the graph is a DAG, a solution will be contained in the list L (although the solution is not necessarily unique). Otherwise, the graph must have at least one cycle and therefore a topological sort is impossible.
Reflecting the non-uniqueness of the resulting sort, the structure S can be simply a set or a queue or a stack. Depending on the order that nodes n are removed from set S, a different solution is created. A variation of Kahn's algorithm that breaks ties lexicographically forms a key component of the Coffman–Graham algorithm for parallel scheduling and layered graph drawing.


=== Depth-first search ===
An alternative algorithm for topological sorting is based on depth-first search. The algorithm loops through each node of the graph, in an arbitrary order, initiating a depth-first search that terminates when it hits any node that has already been visited since the beginning of the topological sort or the node has no outgoing edges (i.e., a leaf node):

L ← Empty list that will contain the sorted nodes
while exists nodes without a permanent mark do
    select an unmarked node n
    visit(n)

function visit(node n)
    if n has a permanent mark then
        return
    if n has a temporary mark then
        stop   (graph has at least one cycle)

    mark n with a temporary mark

    for each node m with an edge from n to m do
        visit(m)

    mark n with a permanent mark
    add n to head of L

Each node n gets prepended to the output list L only after considering all other nodes that depend on n (all descendants of n in the graph).  Specifically, when the algorithm adds node n, we are guaranteed that all nodes that depend on n are already in the output list L: they were added to L either by the recursive call to visit() that ended before the call to visit n, or by a call to visit() that started even before the call to visit n.  Since each edge and node is visited once, the algorithm runs in linear time. This depth-first-search-based algorithm is the one described by Cormen et al. (2001); it seems to have been first described in print by Tarjan in 1976.


=== Parallel algorithms ===
On a parallel random-access machine, a topological ordering can be constructed in O((log n)2) time using a polynomial number of processors, putting the problem into the complexity class NC2.
One method for doing this is to repeatedly square the adjacency matrix of the given graph, logarithmically many times, using min-plus matrix multiplication with maximization in place of minimization. The resulting matrix describes the longest path distances in the graph. Sorting the vertices by the lengths of their longest incoming paths produces a topological ordering.
An algorithm for parallel topological sorting on distributed memory machines parallelizes the algorithm of Kahn for a DAG 
  
    
      
        G
        =
        (
        V
        ,
        E
        )
      
    
    {\\displaystyle G=(V,E)}
  
. On a high level, the algorithm of Kahn repeatedly removes the vertices of indegree 0 and adds them to the topological sorting in the order in which they were removed. Since the outgoing edges of the removed vertices are also removed, there will be a new set of vertices of indegree 0, where the procedure is repeated until no vertices are left. This algorithm performs 
  
    
      
        D
        +
        1
      
    
    {\\displaystyle D+1}
  
 iterations, where D is the longest path in G. Each iteration can be parallelized, which is the idea of the following algorithm.
In the following, it is assumed that the graph partition is stored on p processing elements (PE), which are labeled 
  
    
      
        0
        ,
        …
        ,
        p
        −
        1
      
    
    {\\displaystyle 0,\\dots ,p-1}
  
. Each PE i initializes a set of local vertices 
  
    
      
        
          Q
          
            i
          
          
            1
          
        
      
    
    {\\displaystyle Q_{i}^{1}}
  
 with indegree 0, where the upper index represents the current iteration.""",
    tier=6,
    domain="graph_theory",
    source="Wikipedia, 'Topological sorting'",
    source_url="https://en.wikipedia.org/wiki/Topological_sorting",
))

register_atom(Atom(
    atom_type="algorithm",
    name="knapsack",
    content="""The knapsack problem is the following problem in combinatorial optimization:

Given a set of items, each with a weight and a value, determine which items to include in the collection so that the total weight is less than or equal to a given limit and the total value is as large as possible.
It derives its name from the problem faced by someone who is constrained by a fixed-size knapsack and must fill it with the most valuable items. The problem often arises in resource allocation where the decision-makers have to choose from a set of non-divisible projects or tasks under a fixed budget or time constraint, respectively.
The knapsack problem has been studied for more than a century, with early works dating as far back as 1897.
The subset sum problem is a special case of the decision and 0-1 problems where for each kind of item, the weight equals the value: 
  
    
      
        
          w
          
            i
          
        
        =
        
          v
          
            i
          
        
      
    
    {\\displaystyle w_{i}=v_{i}}
  
.  In the field of cryptography, the term knapsack problem is often used to refer specifically to the subset sum problem. The subset sum problem is one of Karp's 21 NP-complete problems.


== Applications ==
Knapsack problems appear in real-world decision-making processes in a wide variety of fields, such as finding the least wasteful way to cut raw materials, selection of investments and portfolios, selection of assets for asset-backed securitization, and generating keys for the Merkle–Hellman and other knapsack cryptosystems.
One early application of knapsack algorithms was in the construction and scoring of tests in which the test-takers have a choice as to which questions they answer. For small examples, it is a fairly simple process to provide the test-takers with such a choice. For example, if an exam contains 12 questions each worth 10 points, the test-taker need only answer 10 questions to achieve a maximum possible score of 100 points. However, on tests with a heterogeneous distribution of point values, it is more difficult to provide choices. Feuerman and Weiss proposed a system in which students are given a heterogeneous test with a total of 125 possible points. The students are asked to answer all of the questions to the best of their abilities. Of the possible subsets of problems whose total point values add up to 100, a knapsack algorithm would determine which subset gives each student the highest possible score.
A 1999 study of the Stony Brook University Algorithm Repository showed that, out of 75 algorithmic problems related to the field of combinatorial algorithms and algorithm engineering, the knapsack problem was the 19th most popular and the third most needed after suffix trees and the bin packing problem.


== Definition ==
The most common problem being solved is the 0-1 knapsack problem, which restricts the number 
  
    
      
        
          x
          
            i
          
        
      
    
    {\\displaystyle x_{i}}
  
 of copies of each kind of item to zero or one. Given a set of 
  
    
      
        n
      
    
    {\\displaystyle n}
  
 items numbered from 1 up to 
  
    
      
        n
      
    
    {\\displaystyle n}
  
, each with a weight 
  
    
      
        
          w
          
            i
          
        
      
    
    {\\displaystyle w_{i}}
  
 and a value 
  
    
      
        
          v
          
            i
          
        
      
    
    {\\displaystyle v_{i}}
  
, along with a maximum weight capacity 
  
    
      
        W
      
    
    {\\displaystyle W}
  
,

maximize 
  
    
      
        
          ∑
          
            i
            =
            1
          
          
            n
          
        
        
          v
          
            i
          
        
        
          x
          
            i
          
        
      
    
    {\\displaystyle \\sum _{i=1}^{n}v_{i}x_{i}}
  

subject to 
  
    
      
        
          ∑
          
            i
            =
            1
          
          
            n
          
        
        
          w
          
            i
          
        
        
          x
          
            i
          
        
        ≤
        W
      
    
    {\\displaystyle \\sum _{i=1}^{n}w_{i}x_{i}\\leq W}
  
 and 
  
    
      
        
          x
          
            i
          
        
        ∈
        {
        0
        ,
        1
        }
      
    
    {\\displaystyle x_{i}\\in \\{0,1\\}}
  
.
Here 
  
    
      
        
          x
          
            i
          
        
      
    
    {\\displaystyle x_{i}}
  
 represents the number of instances of item 
  
    
      
        i
      
    
    {\\displaystyle i}
  
 to include in the knapsack.""",
    tier=6,
    domain="dynamic_programming",
    source="Wikipedia, 'Knapsack problem'",
    source_url="https://en.wikipedia.org/wiki/Knapsack_problem",
))

register_atom(Atom(
    atom_type="algorithm",
    name="lcs",
    content="""A longest common subsequence (LCS) is the longest subsequence common to all sequences in a set of sequences (often just two sequences). It differs from the longest common substring: unlike substrings, subsequences are not required to occupy consecutive positions within the original sequences. The problem of computing longest common subsequences is a classic computer science problem. Because it is polynomial and has an efficient algorithm to solve it, it is employed to compare data and merge changes to files in programs such as the diff utility and revision control systems such as Git. It has similar applications in computational linguistics and bioinformatics.
For example, consider the sequences (ABCD) and (ACBAD). They have five length-2 common subsequences: (AB), (AC), (AD), (BD), and (CD); two length-3 common subsequences: (ABD) and (ACD); and no longer common subsequences. So (ABD) and (ACD) are their longest common subsequences.


== Complexity ==
For the general case of an arbitrary number of input sequences, the problem is NP-hard. When the number of sequences is constant, the problem is solvable in polynomial time by dynamic programming.
Given 
  
    
      
        N
      
    
    {\\displaystyle N}
  
 sequences of lengths 
  
    
      
        
          n
          
            1
          
        
        ,
        .
        .
        .
        ,
        
          n
          
            N
          
        
      
    
    {\\displaystyle n_{1},...,n_{N}}
  
, a naive search would test each of the 
  
    
      
        
          2
          
            
              n
              
                1
              
            
          
        
      
    
    {\\displaystyle 2^{n_{1}}}
  
 subsequences of the first sequence to determine whether they are also subsequences of the remaining sequences; each subsequence may be tested in time linear in the lengths of the remaining sequences, so the time for this algorithm would be

  
    
      
        O
        
          (
          
            
              2
              
                
                  n
                  
                    1
                  
                
              
            
            
              ∑
              
                i
                >
                1
              
            
            
              n
              
                i
              
            
          
          )
        
        .
      
    
    {\\displaystyle O\\left(2^{n_{1}}\\sum _{i>1}n_{i}\\right).}
  

For the case of two sequences of n and m elements, the running time of the dynamic programming approach is O(n × m). For an arbitrary number of input sequences, the dynamic programming approach gives a solution in

  
    
      
        O
        
          (
          
            N
            
              ∏
              
                i
                =
                1
              
              
                N
              
            
            
              n
              
                i
              
            
          
          )
        
        .
      
    
    {\\displaystyle O\\left(N\\prod _{i=1}^{N}n_{i}\\right).}
  

There exist methods with lower complexity,
which often depend on the length of the LCS, the size of the alphabet, or both.
The LCS is not necessarily unique; in the worst case, the number of common subsequences is exponential in the lengths of the inputs, so the algorithmic complexity of listing all common subsequences must be at least exponential.


== Solution for two sequences ==
The LCS problem has an optimal substructure: the problem can be broken down into smaller, simpler subproblems, which can, in turn, be broken down into simpler subproblems, and so on, until, finally, the solution becomes trivial. LCS in particular has overlapping subproblems: the solutions to high-level subproblems often reuse solutions to lower level subproblems. Problems with these two properties are amenable to dynamic programming approaches, in which subproblem solutions are memoized, that is, the solutions of subproblems are saved for reuse.


=== Prefixes ===
The prefix Sn of S is defined as the first n characters of S.  For example, the prefixes of S = (AGCA) are

S0 = ()
S1 = (A)
S2 = (AG)
S3 = (AGC)
S4 = (AGCA).
Let LCS(X, Y) be a function that computes a longest subsequence common to X and Y.  Such a function has two interesting properties.


=== First property ===
LCS(X^A,Y^A) = LCS(X,Y)^A, for all strings X, Y and all symbols A, where ^ denotes string concatenation. This allows one to simplify the LCS computation for two sequences ending in the same symbol.
For example, LCS("BANANA","ATANA") = LCS("BANAN","ATAN")^"A",  Continuing for the remaining common symbols, LCS("BANANA","ATANA") = LCS("BAN","AT")^"ANA".


=== Second property ===
If A and B are distinct symbols (A≠B), then LCS(X^A,Y^B) is one of the maximal-length strings in the set { LCS(X^A,Y), LCS(X,Y^B) }, for all strings X, Y.
For example, 
LCS("ABCDEFG","BCDGK") is the longest string among LCS("ABCDEFG","BCDG") and LCS("ABCDEF","BCDGK"); if both happened to be of equal length, one of them could be chosen arbitrarily.
To realize the property, distinguish two cases:

If  LCS("ABCDEFG","BCDGK") ends with a "G", then the final "K" cannot be in the LCS, hence LCS("ABCDEFG","BCDGK") = LCS("ABCDEFG","BCDG").
If  LCS("ABCDEFG","BCDGK") does not end with a "G", then the final "G" cannot be in the LCS, hence LCS("ABCDEFG","BCDGK") = LCS("ABCDEF","BCDGK").


=== LCS function defined ===
Let two sequences be defined as follows:  
  
    
      
        X
        =
        (
        
          x
          
            1
          
        
        
          x
          
            2
          
        
        ⋯
        
          x
          
            m
          
        
        )
      
    
    {\\displaystyle X=(x_{1}x_{2}\\cdots x_{m})}
  
 and 
  
    
      
        Y
        =
        (
        
          y
          
            1
          
        
        
          y
          
            2
          
        
        ⋯
        
          y
          
            n
          
        
        )
      
    
    {\\displaystyle Y=(y_{1}y_{2}\\cdots y_{n})}
  
.  The prefixes of 
  
    
      
        X
      
    
    {\\displaystyle X}
  
 are 
  
    
      
        
          X
          
            0
          
        
        ,
        
          X
          
            1
          
        
        ,
        
          X
          
            2
          
        
        ,
        …
        ,
        
          X
          
            m
          
        
      
    
    {\\displaystyle X_{0},X_{1},X_{2},\\dots ,X_{m}}
  
; the prefixes of 
  
    
      
        Y
      
    
    {\\displaystyle Y}
  
 are 
  
    
      
        
          Y
          
            0
          
        
        ,
        
          Y
          
            1
          
        
        ,
        
          Y
          
            2
          
        
        ,
        …
        ,
        
          Y
          
            n
          
        
      
    
    {\\displaystyle Y_{0},Y_{1},Y_{2},\\dots ,Y_{n}}
  
.  Let 
  
    
      
        
          
            L
            C
            S
          
        
        (
        
          X
          
            i
          
        
        ,
        
          Y
          
            j
          
        
        )
      
    
    {\\displaystyle {\\mathit {LCS}}(X_{i},Y_{j})}
  
 represent the set of longest common subsequence of prefixes 
  
    
      
        
          X
          
            i
          
        
      
    
    {\\displaystyle X_{i}}
  
 and 
  
    
      
        
          Y
          
            j
          
        
      
    
    {\\displaystyle Y_{j}}
  
.""",
    tier=6,
    domain="dynamic_programming",
    source="Wikipedia, 'Longest common subsequence'",
    source_url="https://en.wikipedia.org/wiki/Longest_common_subsequence",
))

register_atom(Atom(
    atom_type="algorithm",
    name="lis",
    content="""In computer science, the longest increasing subsequence problem aims to find a subsequence of a given sequence in which the subsequence's elements are sorted in an ascending order and in which the subsequence is as long as possible. This subsequence is not necessarily contiguous or unique. The longest increasing subsequences are studied in the context of various disciplines related to mathematics, including algorithmics, random matrix theory, representation theory, and physics. The longest increasing subsequence problem is solvable in time 
  
    
      
        O
        (
        n
        log
        ⁡
        n
        )
        ,
      
    
    {\\displaystyle O(n\\log n),}
  
 where 
  
    
      
        n
      
    
    {\\displaystyle n}
  
 denotes the length of the input sequence.


== Example ==
In the first 16 terms of the binary Van der Corput sequence

0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15
one of the longest increasing subsequences is

0, 2, 6, 9, 11, 15.
This subsequence has length six; the input sequence has no seven-member increasing subsequences. The longest increasing subsequence in this example is not the only solution: for instance,

0, 4, 6, 9, 11, 15
0, 2, 6, 9, 13, 15
0, 4, 6, 9, 13, 15
are other increasing subsequences of equal length in the same input sequence.


== Relations to other algorithmic problems ==
The longest increasing subsequence problem is closely related to the longest common subsequence problem, which has a quadratic time dynamic programming solution: the longest increasing subsequence of a sequence 
  
    
      
        S
      
    
    {\\displaystyle S}
  
 is the longest common subsequence of 
  
    
      
        S
      
    
    {\\displaystyle S}
  
 and 
  
    
      
        T
        ,
      
    
    {\\displaystyle T,}
  
 where 
  
    
      
        T
      
    
    {\\displaystyle T}
  
 is the result of sorting 
  
    
      
        S
        .
      
    
    {\\displaystyle S.}
  
 However, for the special case in which the input is a permutation of the integers 
  
    
      
        1
        ,
        2
        ,
        …
        ,
        n
        ,
      
    
    {\\displaystyle 1,2,\\ldots ,n,}
  
 this approach can be made much more efficient, leading to time bounds of the form 
  
    
      
        O
        (
        n
        log
        ⁡
        log
        ⁡
        n
        )
        .
      
    
    {\\displaystyle O(n\\log \\log n).}
  

The largest clique in a permutation graph corresponds to the longest decreasing subsequence of the permutation that defines the graph (assuming the original non-permuted sequence is sorted from lowest value to highest). Similarly, the maximum independent set in a permutation graph corresponds to the longest non-decreasing subsequence. Therefore, longest increasing subsequence algorithms can be used to solve the clique problem efficiently in permutation graphs.
In the Robinson–Schensted correspondence between permutations and Young tableaux, the length of the first row of the tableau corresponding to a permutation equals the length of the longest increasing subsequence of the permutation, and the length of the first column equals the length of the longest decreasing subsequence.


== Efficient algorithms ==
The algorithm outlined below solves the longest increasing subsequence problem efficiently with arrays and binary searching. 
It processes the sequence elements in order, maintaining the longest increasing subsequence found so far. Denote the sequence values as 
  
    
      
        X
        [
        0
        ]
        ,
        X
        [
        1
        ]
        ,
        …
        ,
      
    
    {\\displaystyle X[0],X[1],\\ldots ,}
  
 etc. Then, after processing 
  
    
      
        X
        [
        i
        ]
        ,
      
    
    {\\displaystyle X[i],}
  
 the algorithm will have stored an integer 
  
    
      
        L
      
    
    {\\displaystyle L}
  
 and values in two arrays:

  
    
      
        L
      
    
    {\\displaystyle L}
  
 — stores the length of the longest increasing subsequence found so far.

  
    
      
        M
        [
        l
        ]
      
    
    {\\displaystyle M[l]}
  
 — stores the index 
  
    
      
        k
      
    
    {\\displaystyle k}
  
 of the smallest value 
  
    
      
        X
        [
        k
        ]
      
    
    {\\displaystyle X[k]}
  
 such that there is an increasing subsequence of length 
  
    
      
        l
      
    
    {\\displaystyle l}
  
 ending at 
  
    
      
        X
        [
        k
        ]
      
    
    {\\displaystyle X[k]}
  
 in the range 
  
    
      
        k
        ≤
        i
        .
      
    
    {\\displaystyle k\\leq i.}
  
 Explicitly, suppose that 
  
    
      
        
          K
          
            i
            ,
            l
          
        
      
    
    {\\displaystyle K_{i,l}}
  
 denotes the set of all indices 
  
    
      
        j
      
    
    {\\displaystyle j}
  
 such that 
  
    
      
        j
        ≤
        i
      
    
    {\\displaystyle j\\leq i}
  
 and there exists an increasing subsequence of length 
  
    
      
        l
      
    
    {\\displaystyle l}
  
 ending at 
  
    
      
        X
        [
        j
        ]
        .
      
    
    {\\displaystyle X[j].}
  
 Then 
  
    
      
        k
        =
        M
        [
        l
        ]
      
    
    {\\displaystyle k=M[l]}
  
 is the index in 
  
    
      
        
          K
          
            i
            ,
            l
          
        
      
    
    {\\displaystyle K_{i,l}}
  
 for which 
  
    
      
        X
        [
        M
        [
        l
        ]
        ]
      
    
    {\\displaystyle X[M[l]]}
  
 is minimized; meaning that 
  
    
      
        M
        [
        l
        ]
        ∈
        
          K
          
            i
            ,
            l
          
        
      
    
    {\\displaystyle M[l]\\in K_{i,l}}
  
 and 
  
    
      
        X
        [
        M
        [
        l
        ]
        ]
        =
        
          min
          
            j
            ∈
            
              K
              
                i
                ,
                l
              
            
          
        
        X
        [
        j
        ]
      
    
    {\\displaystyle X[M[l]]=\\min _{j\\in K_{i,l}}X[j]}
  
 (or equivalently, 
  
    
      
        M
        [
        l
        ]
        ∈
        
          K
          
            i
            ,
            l
          
        
      
    
    {\\displaystyle M[l]\\in K_{i,l}}
  
 and for every 
  
    
      
        j
        ∈
        
          K
          
            i
            ,
            l
          
        
        ,
      
    
    {\\displaystyle j\\in K_{i,l},}
  
 
  
    
      
        X
        [
        M
        [
        l
        ]
        ]
        ≤
        X
        [
        j
        ]
      
    
    {\\displaystyle X[M[l]]\\leq X[j]}
  
); if multiple indices satisfy this condition then 
  
    
      
        M
        [
        l
        ]
      
    
    {\\displaystyle M[l]}
  
 is the largest one.
To clarify, "there exists an increasing subsequence of length 
  
    
      
        l
      
    
    {\\displaystyle l}
  
 ending at 
  
    
      
        X
        [
        k
        ]
      
    
    {\\displaystyle X[k]}
  
" means that there exist 
  
    
      
        l
      
    
    {\\displaystyle l}
  
 indices 
  
    
      
        
          i
          
            1
          
        
        <
        
          i
          
            2
          
        
        <
        ⋯
        <
        
          i
          
            l
          
        
        =
        k
      
    
    {\\displaystyle i_{1}<i_{2}<\\cdots <i_{l}=k}
  
 ending at 
  
    
      
        k
      
    
""",
    tier=6,
    domain="dynamic_programming",
    source="Wikipedia, 'Longest increasing subsequence'",
    source_url="https://en.wikipedia.org/wiki/Longest_increasing_subsequence",
))

register_atom(Atom(
    atom_type="algorithm",
    name="partial_fractions",
    content="""In algebra, the partial fraction decomposition or partial fraction expansion of a rational fraction (that is, a fraction such that the numerator and the denominator are both polynomials) is an operation that consists of expressing the fraction as a sum of a polynomial (possibly zero) and one or several fractions with a simpler denominator.
The importance of the partial fraction decomposition lies in the fact that it provides algorithms for various computations with rational functions, including the explicit computation of antiderivatives,  Taylor series expansions, inverse Z-transforms, and inverse Laplace transforms. The concept was discovered independently in 1702 by both Johann Bernoulli and Gottfried Leibniz.
In symbols, the partial fraction decomposition of a rational fraction of the form 
  
    
      
        
          
            
              f
              (
              x
              )
            
            
              g
              (
              x
              )
            
          
        
        ,
      
    
    {\\textstyle {\\frac {f(x)}{g(x)}},}
  
 where f and g are polynomials, is the expression of the rational fraction as

  
    
      
        
          
            
              f
              (
              x
              )
            
            
              g
              (
              x
              )
            
          
        
        =
        p
        (
        x
        )
        +
        
          ∑
          
            j
          
        
        
          
            
              
                f
                
                  j
                
              
              (
              x
              )
            
            
              
                g
                
                  j
                
              
              (
              x
              )
            
          
        
      
    
    {\\displaystyle {\\frac {f(x)}{g(x)}}=p(x)+\\sum _{j}{\\frac {f_{j}(x)}{g_{j}(x)}}}
  

where
p(x) is a polynomial, and, for each j,
the denominator gj (x) is a power of an irreducible polynomial (i.e. not factorizable into polynomials of positive degrees), and
the numerator fj (x) is a polynomial of a smaller degree than the degree of this irreducible polynomial.
When explicit computation is involved, a coarser decomposition is often preferred, which consists of replacing "irreducible polynomial" by "square-free polynomial" in the description of the outcome. This allows replacing polynomial factorization by the much easier-to-compute square-free factorization. This is sufficient for most applications, and avoids introducing irrational coefficients when the coefficients of the input polynomials are integers or rational numbers.


== Basic principles ==
Let 

  
    
      
        R
        (
        x
        )
        =
        
          
            F
            G
          
        
      
    
    {\\displaystyle R(x)={\\frac {F}{G}}}
  
 
be a rational fraction, where F and G are univariate polynomials in the indeterminate x over a field. The existence of the partial fraction decomposition can be proved by applying inductively the following reduction steps.


=== Polynomial part ===
There exist two polynomials E and F1 such that 

  
    
      
        
          
            F
            G
          
        
        =
        E
        +
        
          
            
              F
              
                1
              
            
            G
          
        
        ,
      
    
    {\\displaystyle {\\frac {F}{G}}=E+{\\frac {F_{1}}{G}},}
  

and

  
    
      
        deg
        ⁡
        
          F
          
            1
          
        
        <
        deg
        ⁡
        G
        ,
      
    
    {\\displaystyle \\deg F_{1}<\\deg G,}
  

where 
  
    
      
        deg
        ⁡
        P
      
    
    {\\displaystyle \\deg P}
  
 denotes the degree of the polynomial P.
This results immediately from the Euclidean division  of F by G, which asserts the existence of E and F1 such that 
  
    
      
        F
        =
        E
        G
        +
        
          F
          
            1
          
        
      
    
    {\\displaystyle F=EG+F_{1}}
  
 and 
  
    
      
        deg
        ⁡
        
          F
          
            1
          
        
        <
        deg
        ⁡
        G
        .
      
    
    {\\displaystyle \\deg F_{1}<\\deg G.}
  

This allows supposing in the next steps that 
  
    
      
        deg
        ⁡
        F
        <
        deg
        ⁡
        G
        .
      
    
    {\\displaystyle \\deg F<\\deg G.}
  


=== Factors of the denominator ===
If 
  
    
      
        deg
        ⁡
        F
        <
        deg
        ⁡
        G
        ,
      
    
    {\\displaystyle \\deg F<\\deg G,}
  
 and 

  
    
      
        G
        =
        
          G
          
            1
          
        
        
          G
          
            2
          
        
        ,
      
    
    {\\displaystyle G=G_{1}G_{2},}
  

where G1 and G2 are coprime polynomials, then there exist polynomials 
  
    
      
        
          F
          
            1
          
        
      
    
    {\\displaystyle F_{1}}
  
 and 
  
    
      
        
          F
          
            2
          
        
      
    
    {\\displaystyle F_{2}}
  
 such that

  
    
      
        
          
            F
            G
          
        
        =
        
          
            
              F
              
                1
              
            
            
              G
              
                1
              
            
          
        
        +
        
          
            
              F
              
                2
              
            
            
              G
              
                2
              
            
          
        
        ,
      
    
    {\\displaystyle {\\frac {F}{G}}={\\frac {F_{1}}{G_{1}}}+{\\frac {F_{2}}{G_{2}}},}
  

and

  
    
      
        deg
        ⁡
        
          F
          
            1
          
        
        <
        deg
        ⁡
        
          G
          
            1
          
        
        
        
          and
        
        
        deg
        ⁡
        
          F
          
            2
          
        
        <
        deg
        ⁡
        
          G
          
            2
          
        
        .
      
    
    {\\displaystyle \\deg F_{1}<\\deg G_{1}\\quad {\\text{and}}\\quad \\deg F_{2}<\\deg G_{2}.}
  

This can be proved as follows.""",
    tier=6,
    domain="calculus",
    source="Wikipedia, 'Partial fraction decomposition'",
    source_url="https://en.wikipedia.org/wiki/Partial_fraction_decomposition",
))

register_atom(Atom(
    atom_type="theorem",
    name="de_moivre",
    content="""In mathematics, de Moivre's formula (also known as de Moivre's theorem and de Moivre's identity) states that for any real number x and integer n,

  
    
      
        
          
            (
          
        
        cos
        ⁡
        x
        +
        i
        sin
        ⁡
        x
        
          
            
              )
            
          
          
            n
          
        
        =
        cos
        ⁡
        n
        x
        +
        i
        sin
        ⁡
        n
        x
        ,
      
    
    {\\displaystyle {\\big (}\\cos x+i\\sin x{\\big )}^{n}=\\cos nx+i\\sin nx,}
  

where i is the imaginary unit (i2 = −1). The formula is named after Abraham de Moivre, although he never stated it in his works. The expression cos x + i sin x is sometimes abbreviated to cis x.
The formula is important because it connects complex numbers and trigonometry. By expanding the left hand side and then comparing the real and imaginary parts under the assumption that x is real, it is possible to derive useful expressions for cos nx and sin nx in terms of cos x and sin x.
As written, the formula is not valid for non-integer powers n. However, there are generalizations of this formula valid for other exponents. These can be used to give explicit expressions for the nth roots of unity, that is, complex numbers z such that zn = 1.
Using the standard extensions of the sine and cosine functions to complex numbers, the formula is valid even when x is an arbitrary complex number.


== Example ==
For 
  
    
      
        x
        =
        
          
            π
            6
          
        
      
    
    {\\displaystyle x={\\frac {\\pi }{6}}}
  
 and 
  
    
      
        n
        =
        2
      
    
    {\\displaystyle n=2}
  
, de Moivre's formula asserts that

  
    
      
        
          
            (
            
              cos
              ⁡
              
                
                  (
                
              
              
                
                  π
                  6
                
              
              
                
                  )
                
              
              +
              i
              sin
              ⁡
              
                
                  (
                
              
              
                
                  π
                  6
                
              
              
                
                  )
                
              
            
            )
          
          
            2
          
        
        =
        cos
        ⁡
        
          
            (
          
        
        2
        ⋅
        
          
            π
            6
          
        
        
          
            )
          
        
        +
        i
        sin
        ⁡
        
          
            (
          
        
        2
        ⋅
        
          
            π
            6
          
        
        
          
            )
          
        
        ,
      
    
    {\\displaystyle \\left(\\cos {\\bigg (}{\\frac {\\pi }{6}}{\\bigg )}+i\\sin {\\bigg (}{\\frac {\\pi }{6}}{\\bigg )}\\right)^{2}=\\cos {\\bigg (}2\\cdot {\\frac {\\pi }{6}}{\\bigg )}+i\\sin {\\bigg (}2\\cdot {\\frac {\\pi }{6}}{\\bigg )},}
  

or equivalently that

  
    
      
        
          
            (
            
              
                
                  
                    3
                  
                  2
                
              
              +
              
                
                  i
                  2
                
              
            
            )
          
          
            2
          
        
        =
        
          
            1
            2
          
        
        +
        
          
            
              i
              
                
                  3
                
              
            
            2
          
        
        .
      
    
    {\\displaystyle \\left({\\frac {\\sqrt {3}}{2}}+{\\frac {i}{2}}\\right)^{2}={\\frac {1}{2}}+{\\frac {i{\\sqrt {3}}}{2}}.}
  

In this example, it is easy to check the validity of the equation by multiplying out the left side.


== Relation to Euler's formula ==
De Moivre's formula is a precursor to Euler's formula

  
    
      
        
          e
          
            i
            x
          
        
        =
        cos
        ⁡
        x
        +
        i
        sin
        ⁡
        x
        ,
      
    
    {\\displaystyle e^{ix}=\\cos x+i\\sin x,}
  

with x expressed in radians rather than degrees, which establishes the fundamental relationship between the trigonometric functions and the complex exponential function. 
One can derive de Moivre's formula using Euler's formula and the exponential law for integer powers

  
    
      
        
          
            (
            
              e
              
                i
                x
              
            
            )
          
          
            n
          
        
        =
        
          e
          
            i
            n
            x
          
        
        ,
      
    
    {\\displaystyle \\left(e^{ix}\\right)^{n}=e^{inx},}
  

since Euler's formula implies that the left side is equal to 
  
    
      
        
          
            (
            
              cos
              ⁡
              x
              +
              i
              sin
              ⁡
              x
            
            )
          
          
            n
          
        
      
    
    {\\displaystyle \\left(\\cos x+i\\sin x\\right)^{n}}
  
 while the right side is equal to 
  
    
      
        cos
        ⁡
        n
        x
        +
        i
        sin
        ⁡
        n
        x
        .
      
    
    {\\displaystyle \\cos nx+i\\sin nx.}
  


== Proof by induction ==
The truth of de Moivre's theorem can be established by using mathematical induction for natural numbers, and extended to all integers from there. For an integer n, call the following statement S(n):

  
    
      
        (
        cos
        ⁡
        x
        +
        i
        sin
        ⁡
        x
        
          )
          
            n
          
        
        =
        cos
        ⁡
        n
        x
        +
        i
        sin
        ⁡
        n
        x
        .
      
    
    {\\displaystyle (\\cos x+i\\sin x)^{n}=\\cos nx+i\\sin nx.}
  

For n > 0, we proceed by mathematical induction. S(1) is clearly true. For our hypothesis, we assume S(k) is true for some natural k.""",
    tier=6,
    domain="complex_analysis",
    source="Wikipedia, 'De Moivre's formula'",
    source_url="https://en.wikipedia.org/wiki/De_Moivre%27s_formula",
))

register_atom(Atom(
    atom_type="algorithm",
    name="group_order",
    content="""In mathematics, the order of a finite group is the number of its elements. If a group is not finite, one says that its order is infinite. The order of an element of a group (also called period length or period) is the order of the subgroup generated by the element. If the group operation is denoted as a multiplication, the order of an element a of a group, is thus the smallest positive integer m such that am = e, where e denotes the identity element of the group, and am denotes the product of m copies of a. If no such m exists, the order of a is infinite. 
The order of a group G is denoted by ord(G) or |G|, and the order of an element a is denoted by ord(a) or |a|, instead of 
  
    
      
        ord
        ⁡
        (
        ⟨
        a
        ⟩
        )
        ,
      
    
    {\\displaystyle \\operatorname {ord} (\\langle a\\rangle ),}
  
 where the brackets denote the generated group.
Lagrange's theorem states that for any subgroup H of a finite group G, the order of the subgroup divides the order of the group; that is, |H| is a divisor of |G|. In particular, the order |a| of any element is a divisor of |G|.


== Example ==
The symmetric group S3 has the following multiplication table.

This group has six elements, so ord(S3) = 6. By definition, the order of the identity, e, is one, since e 1 = e. Each of s, t, and w squares to e, so these group elements have order two: |s| = |t| = |w| = 2. Finally, u and v have order 3, since u3 = vu = e, and v3 = uv = e.


== Order and structure ==
The order of a group G and the orders of its elements give much information about the structure of the group. Roughly speaking, the more complicated the factorization of |G|, the more complicated the structure of G.
For  |G| = 1, the group is trivial. In any group, only the identity element a = e has ord(a) = 1. If every non-identity element in G is equal to its inverse (so that a2 = e), then ord(a) = 2; this implies G is abelian since 
  
    
      
        a
        b
        =
        (
        a
        b
        
          )
          
            −
            1
          
        
        =
        
          b
          
            −
            1
          
        
        
          a
          
            −
            1
          
        
        =
        b
        a
      
    
    {\\displaystyle ab=(ab)^{-1}=b^{-1}a^{-1}=ba}
  
. The converse is not true; for example, the (additive) cyclic group Z6 of integers modulo 6 is abelian, but the number 2 has order 3:

  
    
      
        2
        +
        2
        +
        2
        =
        6
        ≡
        0
        
          
          (
          mod
          
          6
          )
        
      
    
    {\\displaystyle 2+2+2=6\\equiv 0{\\pmod {6}}}
  
.
The relationship between the two concepts of order is the following: if we write

  
    
      
        ⟨
        a
        ⟩
        =
        {
        
          a
          
            k
          
        
        :
        k
        ∈
        
          Z
        
        }
      
    
    {\\displaystyle \\langle a\\rangle =\\{a^{k}\\colon k\\in \\mathbb {Z} \\}}
  

for the subgroup generated by a, then

  
    
      
        ord
        ⁡
        (
        a
        )
        =
        ord
        ⁡
        (
        ⟨
        a
        ⟩
        )
        .
      
    
    {\\displaystyle \\operatorname {ord} (a)=\\operatorname {ord} (\\langle a\\rangle ).}
  

For any integer k, we have

ak = e   if and only if   ord(a) divides k.
In general, the order of any subgroup of G divides the order of G. More precisely: if H is a subgroup of G, then

ord(G) / ord(H) = [G : H], where [G : H] is called the index of H in G, an integer. This is Lagrange's theorem. (This is, however, only true when G has finite order. If ord(G) = ∞, the quotient ord(G) / ord(H) does not make sense.)
As an immediate consequence of the above, we see that the order of every element of a group divides the order of the group. For example, in the symmetric group shown above, where ord(S3) = 6, the possible orders of the elements are 1, 2, 3 or 6.
The following partial converse is true for finite groups: if d divides the order of a group G and d is a prime number, then there exists an element of order d in G (this is sometimes called Cauchy's theorem). The statement does not hold for composite orders, e.g. the Klein four-group does not have an element of order four. This can be shown by inductive proof. The consequences of the theorem include: the order of a group G is a power of a prime p if and only if ord(a) is some power of p for every a in G.
If a has infinite order, then all non-zero powers of a have infinite order as well. If a has finite order, we have the following formula for the order of the powers of a:

ord(ak) = ord(a) / gcd(ord(a), k)
for every integer k. In particular, a and its inverse a−1 have the same order.
In any group, 

  
    
      
        ord
        ⁡
        (
        a
        b
        )
        =
        ord
        ⁡
        (
        b
        a
        )
      
    
    {\\displaystyle \\operatorname {ord} (ab)=\\operatorname {ord} (ba)}
  

There is no general formula relating the order of a product ab to the orders of a and b. In fact, it is possible that both a and b have finite order while ab has infinite order, or that both a and b have infinite order while ab has finite order. An example of the former is a(x) = 2−x, b(x) = 1−x with ab(x) = x−1 in the group 
  
    
      
        S
        y
        m
        (
        
          Z
        
        )
      
    
    {\\displaystyle Sym(\\mathbb {Z} )}
  
. An example of the latter is a(x) = x+1, b(x) = x−1 with ab(x) = x. If ab = ba, we can at least say that ord(ab) divides lcm(ord(a), ord(b)). As a consequence, one can prove that in a finite abelian group, if m denotes the maximum of all the orders of the group's elements, then every element's order divides m.


== Counting by order of elements ==
Suppose G is a finite group of order n, and d is a divisor of n.  The number of order d elements in G is a multiple of φ(d) (possibly zero), where φ is Euler's totient function, giving the number of positive integers no larger than d and coprime to it.  For example, in the case of S3, φ(3) = 2, and we have exactly two elements of order 3. The theorem provides no useful information about elements of order 2, because φ(2) = 1, and is only of limited utility for composite d such as d = 6, since φ(6) = 2, and there are zero elements of order 6 in S3.


== In relation to homomorphisms ==
Group homomorphisms tend to reduce the orders of elements: if f: G → H is a homomorphism, and a is an element of G of finite order, then ord(f(a)) divides ord(a). If f is injective, then ord(f(a)) = ord(a). This can often be used to prove that there are no homomorphisms or no injective homomorphisms, between two explicitly given groups.""",
    tier=6,
    domain="abstract_algebra",
    source="Wikipedia, 'Order (group theory)'",
    source_url="https://en.wikipedia.org/wiki/Order_%28group_theory%29",
))

register_atom(Atom(
    atom_type="theorem",
    name="fourier_coefficient",
    content="""A Fourier series () is a series expansion of a periodic function into a sum of trigonometric functions. The Fourier series is an example of a trigonometric series. By expressing a function as a sum of sines and cosines, many problems involving the function become easier to analyze because trigonometric functions are well understood. For example, Fourier series were first used by Joseph Fourier to find solutions to the heat equation. This application is possible because the derivatives of trigonometric functions fall into simple patterns. Fourier series cannot be used to approximate arbitrary functions, because most functions have infinitely many terms in their Fourier series, and the series do not always converge. Well-behaved functions, for example smooth functions, have Fourier series that converge to the original function. The coefficients of the Fourier series are determined by integrals of the function multiplied by trigonometric functions, described in Fourier series § Definition.
The study of the convergence of Fourier series focus on the behaviors of the partial sums, which means studying the behavior of the sum as more and more terms from the series are summed. The figures below illustrate some partial Fourier series results for the components of a square wave.

Fourier series are closely related to the Fourier transform, a more general tool that can even find the frequency information for functions that are not periodic. Periodic functions can be identified with functions on a circle; for this reason Fourier series are the subject of Fourier analysis on the circle group, denoted by 
  
    
      
        
          T
        
      
    
    {\\displaystyle \\mathbb {T} }
  
 or 
  
    
      
        
          S
          
            1
          
        
      
    
    {\\displaystyle S_{1}}
  
. The Fourier transform is also part of Fourier analysis, but is defined for functions on 
  
    
      
        
          
            R
          
          
            n
          
        
      
    
    {\\displaystyle \\mathbb {R} ^{n}}
  
.
Since Fourier's time, many different approaches to defining and understanding the concept of Fourier series have been discovered, all of which are consistent with one another, but each of which emphasizes different aspects of the topic. Some of the more powerful and elegant approaches are based on mathematical ideas and tools that were not available in Fourier's time. Fourier originally defined the Fourier series for real-valued functions of real arguments, and used the sine and cosine functions in the decomposition. Many other Fourier-related transforms have since been defined, extending his initial idea to many applications and birthing an area of mathematics called Fourier analysis.


== History ==

The Fourier series is named in honor of Jean-Baptiste Joseph Fourier (1768–1830), who made important contributions to the study of trigonometric series, after preliminary investigations by Leonhard Euler, Jean le Rond d'Alembert, and Daniel Bernoulli. Fourier introduced the series for the purpose of solving the heat equation in a metal plate, publishing his initial results in his 1807 Mémoire sur la propagation de la chaleur dans les corps solides (Treatise on the propagation of heat in solid bodies), and publishing his Théorie analytique de la chaleur (Analytical theory of heat) in 1822. The Mémoire introduced Fourier analysis, specifically Fourier series. Through Fourier's research the fact was established that an arbitrary (at first, continuous and later generalized to any piecewise-smooth) function can be represented by a trigonometric series. The first announcement of this great discovery was made by Fourier in 1807, before the French Academy. Early ideas of decomposing a periodic function into the sum of simple oscillating functions date back to the 3rd century BC, when ancient astronomers proposed an empiric model of planetary motions, based on deferents and epicycles.
Independently of Fourier, astronomer Friedrich Wilhelm Bessel introduced Fourier series to solve Kepler's equation. His work was published in 1819, unaware of Fourier's work which remained unpublished until 1822.
The heat equation is a partial differential equation. Prior to Fourier's work, no solution to the heat equation was known in the general case, although particular solutions were known if the heat source behaved in a simple way, in particular, if the heat source was a sine or cosine wave. These simple solutions are now sometimes called eigensolutions. Fourier's idea was to model a complicated heat source as a superposition (or linear combination) of simple sine and cosine waves, and to write the solution as a superposition of the corresponding eigensolutions. This superposition or linear combination is called the Fourier series.
From a modern point of view, Fourier's results are somewhat informal, due to the lack of a precise notion of function and integral in the early nineteenth century. Later, Peter Gustav Lejeune Dirichlet and Bernhard Riemann expressed Fourier's results with greater precision and formality.
Although the original motivation was to solve the heat equation, it later became obvious that the same techniques could be applied to a wide array of mathematical and physical problems, and especially those involving linear differential equations with constant coefficients, for which the eigensolutions are sinusoids. The Fourier series has many such applications in electrical engineering, vibration analysis, acoustics, optics, signal processing, image processing, quantum mechanics, econometrics, shell theory, etc.


=== Beginnings ===
Joseph Fourier wrote

  
    
      
        φ
        (
        y
        )
        =
        
          a
          
            0
          
        
        cos
        ⁡
        
          
            
              π
              y
            
            2
          
        
        +
        
          a
          
            1
          
        
        cos
        ⁡
        3
        
          
            
              π
              y
            
            2
          
        
        +
        
          a
          
            2
          
        
        cos
        ⁡
        5
        
          
            
              π
              y
            
            2
          
        
        +
        ⋯
        .
      
    
    {\\displaystyle \\varphi (y)=a_{0}\\cos {\\frac {\\pi y}{2}}+a_{1}\\cos 3{\\frac {\\pi y}{2}}+a_{2}\\cos 5{\\frac {\\pi y}{2}}+\\cdots .}
  

Multiplying both sides by 
  
    
      
        cos
        ⁡
        (
        2
        k
        +
        1
        )
        
          
            
              π
              y
            
            2
          
        
      
    
    {\\displaystyle \\cos(2k+1){\\frac {\\pi y}{2}}}
  
, and then integrating from 
  
    
      
        y
        =
        −
        1
      
    
    {\\displaystyle y=-1}
  
 to 
  
    
      
        y
        =
        +
        1
      
    
    {\\displaystyle y=+1}
  
 yields:

  
    
      
        
          a
          
            k
          
        
        =
        
          ∫
          
            −
            1
          
          
            1
          
        
        φ
        (
        y
        )
        cos
        ⁡
        (
        2
        k
        +
        1
        )
        
          
            
              π
              y
            
            2
          
        
        
        d
        y
        .
      
    
    {\\displaystyle a_{k}=\\int _{-1}^{1}\\varphi (y)\\cos(2k+1){\\frac {\\pi y}{2}}\\,dy.}
  

This immediately gives any coefficient ak of the trigonometric series for φ(y) for any function which has such an expansion.""",
    tier=6,
    domain="signal_processing",
    source="Wikipedia, 'Fourier series'",
    source_url="https://en.wikipedia.org/wiki/Fourier_series",
))

register_atom(Atom(
    atom_type="definition",
    name="tensor_product",
    content="""In mathematics, the Kronecker product, sometimes denoted by ⊗, is an operation on two matrices of arbitrary size resulting in a block matrix. It is a specialization of the tensor product (which is denoted by the same symbol) from vectors to matrices and gives the matrix of the tensor product linear map with respect to a standard choice of basis. The Kronecker product is to be distinguished from the usual matrix multiplication, which is an entirely different operation. The Kronecker product is also sometimes called matrix direct product.
The Kronecker product is named after the German mathematician Leopold Kronecker (1823–1891), even though there is little evidence that he was the first to define and use it. The Kronecker product has also been called the Zehfuss matrix, and the Zehfuss product, after Johann Georg Zehfuss, who in 1858 described this matrix operation, but Kronecker product is currently the most widely used term. The misattribution to Kronecker rather than Zehfuss was due to Kurt Hensel.


== Definition ==
If A is an m × n matrix and B is a p × q matrix, then the Kronecker product A ⊗ B is the pm × qn block matrix:

  
    
      
        
          A
        
        ⊗
        
          B
        
        =
        
          
            [
            
              
                
                  
                    a
                    
                      11
                    
                  
                  
                    B
                  
                
                
                  ⋯
                
                
                  
                    a
                    
                      1
                      n
                    
                  
                  
                    B
                  
                
              
              
                
                  ⋮
                
                
                  ⋱
                
                
                  ⋮
                
              
              
                
                  
                    a
                    
                      m
                      1
                    
                  
                  
                    B
                  
                
                
                  ⋯
                
                
                  
                    a
                    
                      m
                      n
                    
                  
                  
                    B
                  
                
              
            
            ]
          
        
        ,
      
    
    {\\displaystyle \\mathbf {A} \\otimes \\mathbf {B} ={\\begin{bmatrix}a_{11}\\mathbf {B} &\\cdots &a_{1n}\\mathbf {B} \\\\\\vdots &\\ddots &\\vdots \\\\a_{m1}\\mathbf {B} &\\cdots &a_{mn}\\mathbf {B} \\end{bmatrix}},}
  

more explicitly:

  
    
      
        
          
            A
          
          ⊗
          
            B
          
        
        =
        
          
            [
            
              
                
                  
                    a
                    
                      11
                    
                  
                  
                    b
                    
                      11
                    
                  
                
                
                  
                    a
                    
                      11
                    
                  
                  
                    b
                    
                      12
                    
                  
                
                
                  ⋯
                
                
                  
                    a
                    
                      11
                    
                  
                  
                    b
                    
                      1
                      q
                    
                  
                
                
                  ⋯
                
                
                  ⋯
                
                
                  
                    a
                    
                      1
                      n
                    
                  
                  
                    b
                    
                      11
                    
                  
                
                
                  
                    a
                    
                      1
                      n
                    
                  
                  
                    b
                    
                      12
                    
                  
                
                
                  ⋯
                
                
                  
                    a
                    
                      1
                      n
                    
                  
                  
                    b
                    
                      1
                      q
                    
                  
                
              
              
                
                  
                    a
                    
                      11
                    
                  
                  
                    b
                    
                      21
                    
                  
                
                
                  
                    a
                    
                      11
                    
                  
                  
                    b
                    
                      22
                    
                  
                
                
                  ⋯
                
                
                  
                    a
                    
                      11
                    
                  
                  
                    b
                    
                      2
                      q
                    
                  
                
                
                  ⋯
                
                
                  ⋯
                
                
                  
                    a
                    
                      1
                      n
                    
                  
                  
                    b
                    
                      21
                    
                  
                
                
                  
                    a
                    
                      1
                      n
                    
                  
                  
                    b
                    
                      22
                    
                  
                
                
                  ⋯
                
                
                  
                    a
                    
                      1
                      n
                    
                  
                  
                    b
                    
                      2
                      q
                    
                  
                
              
              
                
                  ⋮
                
                
                  ⋮
                
                
                  ⋱
                
                
                  ⋮
                
                
                
                
                  ⋮
                
                
                  ⋮
                
                
                  ⋱
                
                
                  ⋮
                
              
              
                
                  
                    a
                    
                      11
                    
                  
                  
                    b
                    
                      p
            """,
    tier=6,
    domain="linear_algebra",
    source="Wikipedia, 'Kronecker product'",
    source_url="https://en.wikipedia.org/wiki/Kronecker_product",
))

register_atom(Atom(
    atom_type="identity",
    name="pauli_product",
    content="""In mathematical physics and mathematics, the Pauli matrices are a set of three 
  
    
      
        2
        ×
        2
      
    
    {\\displaystyle 2\\times 2}
  
 complex matrices that are traceless, Hermitian, involutory and unitary. They are usually denoted by the Greek letter 
  
    
      
        σ
      
    
    {\\displaystyle \\sigma }
  
 (sigma), and occasionally by 
  
    
      
        τ
      
    
    {\\displaystyle \\tau }
  
 (tau) when used in connection with isospin symmetries.
  
    
      
        
          
            
              
                
                  σ
                  
                    1
                  
                
                =
                
                  σ
                  
                    x
                  
                
              
              
                
                =
                
                  
                    (
                    
                      
                        
                          0
                        
                        
                          1
                        
                      
                      
                        
                          1
                        
                        
                          0
                        
                      
                    
                    )
                  
                
                ,
              
            
            
              
                
                  σ
                  
                    2
                  
                
                =
                
                  σ
                  
                    y
                  
                
              
              
                
                =
                
                  
                    (
                    
                      
                        
                          0
                        
                        
                          −
                          i
                        
                      
                      
                        
                          i
                        
                        
                          0
                        
                      
                    
                    )
                  
                
                ,
              
            
            
              
                
                  σ
                  
                    3
                  
                
                =
                
                  σ
                  
                    z
                  
                
              
              
                
                =
                
                  
                    (
                    
                      
                        
                          1
                        
                        
                          0
                        
                      
                      
                        
                          0
                        
                        
                          −
                          1
                        
                      
                    
                    )
                  
                
                .
              
            
          
        
      
    
    {\\displaystyle {\\begin{aligned}\\sigma _{1}=\\sigma _{x}&={\\begin{pmatrix}0&1\\\\1&0\\end{pmatrix}},\\\\\\sigma _{2}=\\sigma _{y}&={\\begin{pmatrix}0&-i\\\\i&0\\end{pmatrix}},\\\\\\sigma _{3}=\\sigma _{z}&={\\begin{pmatrix}1&0\\\\0&-1\\end{pmatrix}}.\\\\\\end{aligned}}}
  

These matrices are named after the physicist Wolfgang Pauli. In quantum mechanics, they occur in the Pauli equation, which takes into account the interaction of the spin of a particle with an external electromagnetic field. They also represent the interaction states of two polarization filters for horizontal/vertical polarization, 45 degree polarization (right/left), and circular polarization (right/left).
Each Pauli matrix is Hermitian, and together with the identity matrix 
  
    
      
        
          I
        
      
    
    {\\displaystyle \\mathbb {I} }
  
 (sometimes considered as the zeroth Pauli matrix 
  
    
      
        
          σ
          
            0
          
        
      
    
    {\\displaystyle \\sigma _{0}}
  
), the Pauli matrices form a basis of the vector space of 
  
    
      
        2
        ×
        2
      
    
    {\\displaystyle 2\\times 2}
  
 Hermitian matrices over the real numbers, under addition. This means that any 
  
    
      
        2
        ×
        2
      
    
    {\\displaystyle 2\\times 2}
  
 Hermitian matrix can be written in a unique way as a linear combination of Pauli matrices, with all coefficients being real numbers.
The Pauli matrices satisfy the useful product relation:

  
    
      
        
          
            
              
                
                  σ
                  
                    i
                  
                
                 
                
                  σ
                  
                    j
                  
                
                =
                
                  δ
                  
                    i
                    j
                  
                
                 
                
                  I
                
                +
                i
                 
                
                  ε
                  
                    i
                    j
                    k
                  
                
                 
                
                  σ
                  
                    k
                  
                
                 
                ,
              
            
          
        
      
    
    {\\displaystyle {\\begin{aligned}\\sigma _{i}\\ \\sigma _{j}=\\delta _{ij}\\ \\mathbb {I} +i\\ \\varepsilon _{ijk}\\ \\sigma _{k}\\ ,\\end{aligned}}}
  

where 
  
    
      
        
          δ
          
            i
            j
          
        
      
    
    {\\displaystyle \\delta _{ij}}
  
 is the Kronecker delta, which equals 
  
    
      
        +
        1
      
    
    {\\displaystyle +1}
  
 if 
  
    
      
        i
        =
        j
      
    
    {\\displaystyle i=j}
  
 otherwise 
  
    
      
        0
      
    
    {\\displaystyle 0}
  
, and the Levi-Civita symbol  
  
    
      
        
          ε
          
            i
            j
            k
          
        
      
    
    {\\displaystyle \\varepsilon _{ijk}}
  
is used.
Hermitian operators represent observables in quantum mechanics, so the Pauli matrices span the space of observables of the complex two-dimensional Hilbert space.""",
    tier=6,
    domain="quantum",
    source="Wikipedia, 'Pauli matrices'",
    source_url="https://en.wikipedia.org/wiki/Pauli_matrices",
))

register_atom(Atom(
    atom_type="algorithm",
    name="bloch_coords",
    content="""In quantum mechanics and computing, the Bloch sphere is a geometrical representation of the pure state space of a two-level quantum mechanical system (qubit), named after the physicist Felix Bloch.
Mathematically each quantum mechanical system is associated with a separable complex Hilbert space 
  
    
      
        H
      
    
    {\\displaystyle H}
  
. A pure state of a quantum system is represented by a non-zero vector 
  
    
      
        ψ
      
    
    {\\displaystyle \\psi }
  
 in 
  
    
      
        H
      
    
    {\\displaystyle H}
  
. The vectors 
  
    
      
        ψ
      
    
    {\\displaystyle \\psi }
  
 and 
  
    
      
        λ
        ψ
      
    
    {\\displaystyle \\lambda \\psi }
  
 (with 
  
    
      
        λ
      
    
    {\\displaystyle \\lambda }
  
 a non-zero complex number) represent the same state. A system with n mutually orthogonal quantum states can be described by a Hilbert space of dimension n. Pure states can be represented as equivalence classes, or, rays in a projective Hilbert space 
  
    
      
        
          P
        
        (
        
          H
          
            n
          
        
        )
        =
        
          C
        
        
          
            P
          
          
            n
            −
            1
          
        
      
    
    {\\displaystyle \\mathbf {P} (H_{n})=\\mathbb {C} \\mathbf {P} ^{n-1}}
  
. For a two-dimensional Hilbert space, the space of all such states is the complex projective line 
  
    
      
        
          C
        
        
          
            P
          
          
            1
          
        
        .
      
    
    {\\displaystyle \\mathbb {C} \\mathbf {P} ^{1}.}
  
 This is the Bloch sphere, which can be mapped to the Riemann sphere.
The Bloch sphere is a unit 2-sphere, with antipodal points corresponding to a pair of mutually orthogonal state vectors.  The north and south poles of the Bloch sphere are typically chosen to correspond to the standard basis vectors 
  
    
      
        
          |
        
        0
        ⟩
      
    
    {\\displaystyle |0\\rangle }
  
 and 
  
    
      
        
          |
        
        1
        ⟩
      
    
    {\\displaystyle |1\\rangle }
  
, respectively, which in turn might correspond e.g. to the spin-up and spin-down states of an electron.  This choice is arbitrary, however.  The points on the surface of the sphere correspond to the pure states of the system, whereas the interior points correspond to the mixed states.  The Bloch sphere may be generalized to an n-level quantum system, but then the visualization is less useful.
The natural metric on the Bloch sphere is the Fubini–Study metric.  The mapping from the unit 3-sphere in the two-dimensional state space 
  
    
      
        
          
            C
          
          
            2
          
        
      
    
    {\\displaystyle \\mathbb {C} ^{2}}
  
 to the Bloch sphere is the Hopf fibration, with each ray of spinors mapping to one point on the Bloch sphere.


== Definition ==
Given an orthonormal basis, any pure state 
  
    
      
        
          |
        
        ψ
        ⟩
      
    
    {\\displaystyle |\\psi \\rangle }
  
 of a two-level quantum system can be written as a superposition of the basis vectors 
  
    
      
        
          |
        
        0
        ⟩
      
    
    {\\displaystyle |0\\rangle }
  
 and 
  
    
      
        
          |
        
        1
        ⟩
      
    
    {\\displaystyle |1\\rangle }
  
, where the coefficient of (or contribution from) each of the two basis vectors is a complex number. This means that the state is described by four real numbers. However, only the relative phase between the coefficients of the two basis vectors has any physical meaning (the phase of the quantum system is not directly measurable), so that there is redundancy in this description. We can take the coefficient of 
  
    
      
        
          |
        
        0
        ⟩
      
    
    {\\displaystyle |0\\rangle }
  
 to be real and non-negative.""",
    tier=6,
    domain="quantum",
    source="Wikipedia, 'Bloch sphere'",
    source_url="https://en.wikipedia.org/wiki/Bloch_sphere",
))

register_atom(Atom(
    atom_type="theorem",
    name="diff_equation",
    content="""In mathematics, separation of variables (also known as the Fourier method) is any of several methods for solving ordinary and partial differential equations, in which algebra allows one to rewrite an equation so that each of two variables occurs on a different side of the equation.


== Ordinary differential equations (ODE) ==
A differential equation for the unknown 
  
    
      
        f
        (
        x
        )
      
    
    {\\displaystyle f(x)}
  
 is separable if it can be written in the form

  
    
      
        
          
            d
            
              d
              x
            
          
        
        f
        (
        x
        )
        =
        g
        (
        x
        )
        h
        (
        f
        (
        x
        )
        )
      
    
    {\\displaystyle {\\frac {d}{dx}}f(x)=g(x)h(f(x))}
  

where 
  
    
      
        g
      
    
    {\\displaystyle g}
  
 and 
  
    
      
        h
      
    
    {\\displaystyle h}
  
 are given functions. This is perhaps more transparent when written using 
  
    
      
        y
        =
        f
        (
        x
        )
      
    
    {\\displaystyle y=f(x)}
  
 as:

  
    
      
        
          
            
              d
              y
            
            
              d
              x
            
          
        
        =
        g
        (
        x
        )
        h
        (
        y
        )
        .
      
    
    {\\displaystyle {\\frac {dy}{dx}}=g(x)h(y).}
  

So now as long as h(y) ≠ 0, we can rearrange terms to obtain:

  
    
      
        
          
            
              d
              y
            
            
              h
              (
              y
              )
            
          
        
        =
        g
        (
        x
        )
        
        d
        x
        ,
      
    
    {\\displaystyle {dy \\over h(y)}=g(x)\\,dx,}
  

where the two variables x and y have been separated. Note  dx (and dy) can be viewed, at a simple level, as just a convenient notation, which provides a handy mnemonic aid for assisting with manipulations. A formal definition of dx as a differential (infinitesimal) is somewhat advanced.


=== Alternative notation ===
Those who dislike differentials as separate entities may prefer to write this as

  
    
      
        
          
            1
            
              h
              (
              y
              )
            
          
        
        
          
            
              d
              y
            
            
              d
              x
            
          
        
        =
        g
        (
        x
        )
        ,
      
    
    {\\displaystyle {\\frac {1}{h(y)}}{\\frac {dy}{dx}}=g(x),}
  

but that fails to make it quite as obvious why this is called "separation of variables". Integrating both sides of the equation with respect to 
  
    
      
        x
      
    
    {\\displaystyle x}
  
, we have

or equivalently,

  
    
      
        ∫
        
          
            1
            
              h
              (
              y
              )
            
          
        
        
        d
        y
        =
        ∫
        g
        (
        x
        )
        
        d
        x
      
    
    {\\displaystyle \\int {\\frac {1}{h(y)}}\\,dy=\\int g(x)\\,dx}
  

because of the substitution rule for integrals.
If one can evaluate the two integrals, one can find a solution to the differential equation.  Observe that this process effectively allows us to treat the derivative 
  
    
      
        
          
            
              d
              y
            
            
              d
              x
            
          
        
      
    
    {\\displaystyle {\\frac {dy}{dx}}}
  
 as a fraction which can be separated.  This allows us to solve separable differential equations more conveniently, as demonstrated in the example below.
(Note that we do not need to use two constants of integration, in equation (A1) as in

  
    
      
        ∫
        
          
            1
            
              h
              (
              y
              )
            
          
        
        
        d
        y
        +
        
          C
          
            1
          
        
        =
        ∫
        g
        (
        x
        )
        
        d
        x
        +
        
          C
          
            2
          
        
        ,
      
    
    {\\displaystyle \\int {\\frac {1}{h(y)}}\\,dy+C_{1}=\\int g(x)\\,dx+C_{2},}
  

because a single constant 
  
    
      
        C
        =
        
          C
          
            2
          
        
        −
        
          C
          
            1
          
        
      
    
    {\\displaystyle C=C_{2}-C_{1}}
  
 is equivalent.)


=== Example ===
Population growth is often modeled by the "logistic" differential equation

  
    
      
        
          
            
              d
              P
            
            
              d
              t
            
          
        
        =
        k
        P
        
          (
          
            1
            −
            
              
                P
                K
              
            
          
          )
        
      
    
    {\\displaystyle {\\frac {dP}{dt}}=kP\\left(1-{\\frac {P}{K}}\\right)}
  

where 
  
    
      
        P
      
    
    {\\displaystyle P}
  
 is the population with respect to time 
  
    
      
        t
      
    
    {\\displaystyle t}
  
, 
  
    
      
        k
      
    
    {\\displaystyle k}
  
 is the rate of growth, and 
  
    
      
        K
      
    
    {\\displaystyle K}
  
 is the carrying capacity of the environment.
Separation of variables now leads to

  
    
      
        
          
            
              
              
                
                ∫
                
                  
                    
                      d
                      P
                    
                    
                      P
                      
                        (
                        
                          1
                          −
                          P
                          
                            /
                          
                          K
                        
                        )
                      
                    
                  
                
                =
                ∫
                k
                
                d
                t
              
            
          
        
      
    
    {\\displaystyle {\\begin{aligned}&\\int {\\frac {dP}{P\\left(1-P/K\\right)}}=\\int k\\,dt\\end{aligned}}}
  

which is readily integrated using partial fractions on the left side yielding

  
    
      
        P
        (
        t
        )
        =
        
          
            K
            
              1
              +
              A
              
                e
                
                  −
                  k
                  t
                
              
            
          
        
      
    
    {\\displaystyle P(t)={\\frac {K}{1+Ae^{-kt}}}}
  

where A is the constant of integration. We can find  
  
    
      
        A
      
    
    {\\displaystyle A}
  
 in terms of 
  
    
      
        P
        
          (
          0
          )
        
        =
        
          P
          
            0
          
        
      
    
    {\\displaystyle P\\left(0\\right)=P_{0}}
  
 at t=0.""",
    tier=6,
    domain="calculus",
    source="Wikipedia, 'Separation of variables'",
    source_url="https://en.wikipedia.org/wiki/Separation_of_variables",
))

register_atom(Atom(
    atom_type="theorem",
    name="quadratic_residue",
    content="""In number theory, Euler's criterion is a formula for determining whether an integer is a quadratic residue modulo a prime. Precisely,
Let p be an odd prime and a be an integer coprime to p. Then

  
    
      
        
          a
          
            
              
                
                  p
                  −
                  1
                
                2
              
            
          
        
        ≡
        
          
            {
            
              
                
                  
                  
                  
                  1
                  
                    
                    (
                    mod
                    
                    p
                    )
                  
                
                
                  
                     if there is an integer 
                  
                  x
                  
                     such that 
                  
                  
                    x
                    
                      2
                    
                  
                  ≡
                  a
                  
                    
                    (
                    mod
                    
                    p
                    )
                  
                  ,
                
              
              
                
                  −
                  1
                  
                    
                    (
                    mod
                    
                    p
                    )
                  
                
                
                  
                     if there is no such integer.
                  
                
              
            
            
          
        
      
    
    {\\displaystyle a^{\\tfrac {p-1}{2}}\\equiv {\\begin{cases}\\;\\;\\,1{\\pmod {p}}&{\\text{ if there is an integer }}x{\\text{ such that }}x^{2}\\equiv a{\\pmod {p}},\\\\-1{\\pmod {p}}&{\\text{ if there is no such integer.}}\\end{cases}}}
  

Euler's criterion can be concisely reformulated using the Legendre symbol:

  
    
      
        
          (
          
            
              a
              p
            
          
          )
        
        ≡
        
          a
          
            
              
                
                  p
                  −
                  1
                
                2
              
            
          
        
        
          
          (
          mod
          
          p
          )
        
        .
      
    
    {\\displaystyle \\left({\\frac {a}{p}}\\right)\\equiv a^{\\tfrac {p-1}{2}}{\\pmod {p}}.}
  

The criterion dates from a 1748 paper by Leonhard Euler.


== Proof ==
The proof uses the fact that the residue classes modulo a prime number are a field. See the article prime field for more details.
Because the modulus is prime, Lagrange's theorem applies: a polynomial of degree k can only have at most k roots. In particular, x2 ≡ a (mod p) has at most 2 solutions for each a. This immediately implies that besides 0 there are at least ⁠p − 1/2⁠ distinct quadratic residues modulo p: each of the p − 1 possible values of x can only be accompanied by one other to give the same residue.
In fact, 
  
    
      
        (
        p
        −
        x
        
          )
          
            2
          
        
        ≡
        
          x
          
            2
          
        
        
          
          (
          mod
          
          p
          )
        
        .
      
    
    {\\displaystyle (p-x)^{2}\\equiv x^{2}{\\pmod {p}}.}
  
This is because 
  
    
      
        (
        p
        −
        x
        
          )
          
            2
          
        
        ≡
        
          p
          
            2
          
        
        −
        
          2
        
        
          x
        
        
          p
        
        +
        
          x
          
            2
          
        
        ≡
        
          x
          
            2
          
        
        
          
          (
          mod
          
          p
          )
        
        .
      
    
    {\\displaystyle (p-x)^{2}\\equiv p^{2}-{2}{x}{p}+x^{2}\\equiv x^{2}{\\pmod {p}}.}
  

So, the 
  
    
      
        
          
            
              
                p
                −
                1
              
              2
            
          
        
      
    
    {\\displaystyle {\\tfrac {p-1}{2}}}
  
 distinct quadratic residues are:

  
    
      
        
          1
          
            2
          
        
        ,
        
          2
          
            2
          
        
        ,
        .
        .
        .
        ,
        (
        
          
            
              
                p
                −
                1
              
              2
            
          
        
        
          )
          
            2
          
        
        
          
          (
          mod
          
          p
          )
        
        .
      
    
    {\\displaystyle 1^{2},2^{2},...,({\\tfrac {p-1}{2}})^{2}{\\pmod {p}}.}
  

As a is coprime to p, Fermat's little theorem says that

  
    
      
        
          a
          
            p
            −
            1
          
        
        ≡
        1
        
          
          (
          mod
          
          p
          )
        
        ,
      
    
    {\\displaystyle a^{p-1}\\equiv 1{\\pmod {p}},}
  

which can be written as

  
    
      
        
          (
          
            
              a
              
                
                  
                    
                      p
                      −
                      1
                    
                    2
                  
                
              
            
            −
            1
          
          )
        
        
          (
          
            
              a
              
                
                  
                    
                      p
                      −
                      1
                    
                    2
                  
                
              
            
            +
            1
          
          )
        
        ≡
        0
        
          
          (
          mod
          
          p
          )
        
        .
      
    
    {\\displaystyle \\left(a^{\\tfrac {p-1}{2}}-1\\right)\\left(a^{\\tfrac {p-1}{2}}+1\\right)\\equiv 0{\\pmod {p}}.}
  

Since the integers mod p form a field, for each a, one or the other of these factors must be zero.""",
    tier=6,
    domain="number_theory",
    source="Wikipedia, 'Euler's criterion'",
    source_url="https://en.wikipedia.org/wiki/Euler%27s_criterion",
))

register_atom(Atom(
    atom_type="theorem",
    name="recurrence_solve",
    content="""In mathematics, a recurrence relation is an equation according to which the 
  
    
      
        n
      
    
    {\\displaystyle n}
  
th term of a sequence of numbers is equal to some combination of the previous terms. Often, only 
  
    
      
        k
      
    
    {\\displaystyle k}
  
 previous terms of the sequence appear in the equation, for a parameter 
  
    
      
        k
      
    
    {\\displaystyle k}
  
 that is independent of 
  
    
      
        n
      
    
    {\\displaystyle n}
  
; this number 
  
    
      
        k
      
    
    {\\displaystyle k}
  
 is called the order of the relation. If the values of the first 
  
    
      
        k
      
    
    {\\displaystyle k}
  
 numbers in the sequence have been given, the rest of the sequence can be calculated by repeatedly applying the equation.
In linear recurrences, the nth term is equated to a linear function of the 
  
    
      
        k
      
    
    {\\displaystyle k}
  
 previous terms. A famous example is the recurrence for the Fibonacci numbers,

  
    
      
        
          F
          
            n
          
        
        =
        
          F
          
            n
            −
            1
          
        
        +
        
          F
          
            n
            −
            2
          
        
      
    
    {\\displaystyle F_{n}=F_{n-1}+F_{n-2}}
  

where the order 
  
    
      
        k
      
    
    {\\displaystyle k}
  
 is two and the linear function merely adds the two previous terms. This example is a linear recurrence with constant coefficients, because the coefficients of the linear function (1 and 1) are constants that do not depend on 
  
    
      
        n
        .
      
    
    {\\displaystyle n.}
  
 For these recurrences, one can express the general term of the sequence as a closed-form expression of 
  
    
      
        n
      
    
    {\\displaystyle n}
  
. As well, linear recurrences with polynomial coefficients depending on 
  
    
      
        n
      
    
    {\\displaystyle n}
  
 are also important, because many common elementary functions and special functions have a Taylor series whose coefficients satisfy such a recurrence relation (see holonomic function).
Solving a recurrence relation means obtaining a closed-form solution: a non-recursive function of 
  
    
      
        n
      
    
    {\\displaystyle n}
  
.
The concept of a recurrence relation can be extended to multidimensional arrays, that is, indexed families that are indexed by tuples of natural numbers.


== Definition ==
A recurrence relation is an equation that expresses each element of a sequence as a function of the preceding ones. More precisely, in the case where only the immediately preceding element is involved, a recurrence relation has the form

  
    
      
        
          u
          
            n
          
        
        =
        φ
        (
        n
        ,
        
          u
          
            n
            −
            1
          
        
        )
        
        
          for
        
        
        n
        >
        0
        ,
      
    
    {\\displaystyle u_{n}=\\varphi (n,u_{n-1})\\quad {\\text{for}}\\quad n>0,}
  

where 

  
    
      
        φ
        :
        
          N
        
        ×
        X
        →
        X
      
    
    {\\displaystyle \\varphi :\\mathbb {N} \\times X\\to X}
  

is a function, where X is a set to which the elements of a sequence must belong. For any 
  
    
      
        
          u
          
            0
          
        
        ∈
        X
      
    
    {\\displaystyle u_{0}\\in X}
  
, this defines a unique sequence with 
  
    
      
        
          u
          
            0
          
        
      
    
    {\\displaystyle u_{0}}
  
 as its first element, called the initial value.
It is easy to modify the definition for getting sequences starting from the term of index 1 or higher.
This defines recurrence relation of first order. A recurrence relation of order k has the form 

  
    
      
        
          u
          
            n
          
        
        =
        φ
        (
        n
        ,
        
          u
          
            n
            −
            1
          
        
        ,
        
          u
          
            n
            −
            2
          
        
        ,
        …
        ,
        
          u
          
            n
            −
            k
          
        
        )
        
        
          for
        
        
        n
        ≥
        k
        ,
      
    
    {\\displaystyle u_{n}=\\varphi (n,u_{n-1},u_{n-2},\\ldots ,u_{n-k})\\quad {\\text{for}}\\quad n\\geq k,}
  

where 
  
    
      
        φ
        :
        
          N
        
        ×
        
          X
          
            k
          
        
        →
        X
      
    
    {\\displaystyle \\varphi :\\mathbb {N} \\times X^{k}\\to X}
  
 is a function that involves k consecutive elements of the sequence.
In this case, k initial values are needed for defining a sequence.


== Examples ==


=== Factorial ===
The factorial is defined by the recurrence relation

  
    
      
        n
        !
        =
        n
        ⋅
        (
        n
        −
        1
        )
        !
        
        
          for
        
        
        n
        >
        0
        ,
      
    
    {\\displaystyle n!=n\\cdot (n-1)!\\quad {\\text{for}}\\quad n>0,}
  

and the initial condition

  
    
      
        0
        !
        =
        1.
      
    
    {\\displaystyle 0!=1.}
  

This is an example of a linear recurrence with polynomial coefficients of order 1, with the simple polynomial (in n)

  
    
      
        n
      
    
    {\\displaystyle n}
  

as its only coefficient.


=== Logistic map ===
An example of a recurrence relation is the logistic map defined by

  
    
      
        
          x
          
            n
            +
            1
          
        
        =
        r
        
          x
          
            n
          
        
        (
        1
        −
        
          x
          
            n
          
        
        )
        ,
      
    
    {\\displaystyle x_{n+1}=rx_{n}(1-x_{n}),}
  

for a given constant 
  
    
      
        r
        .
      
    
    {\\displaystyle r.}
  
 The behavior of the sequence depends dramatically on 
  
    
      
        r
        ,
      
    
    {\\displaystyle r,}
  
 but is stable when the initial condition 
  
    
      
        
          x
          
            0
          
        
      
    
    {\\displaystyle x_{0}}
  
 varies.


=== Fibonacci numbers ===
The recurrence of order two satisfied by the Fibonacci numbers is the canonical example of a homogeneous linear recurrence relation with constant coefficients (see below).""",
    tier=6,
    domain="algebra",
    source="Wikipedia, 'Recurrence relation'",
    source_url="https://en.wikipedia.org/wiki/Recurrence_relation",
))

register_atom(Atom(
    atom_type="algorithm",
    name="polynomial_division",
    content="""In algebra, polynomial long division is an algorithm for dividing a polynomial by another polynomial of the same or lower degree, a generalized version of the familiar arithmetic technique called long division. It can be done easily by hand, because it separates an otherwise complex division problem into smaller ones.  Polynomial long division is an algorithm that implements the Euclidean division of polynomials: starting from two polynomials A (the dividend) and B (the divisor) produces, if B is not zero, a quotient Q and a remainder R such that

A = BQ + R,
and either R = 0 or the degree of R is lower than the degree of B. These conditions uniquely define  Q and R; the result R = 0 occurs if and only if the polynomial A has B as a factor. Thus long division is a means for testing whether one polynomial has another as a factor, and, if it does, for factoring it out. 
Sometimes using a shorthand version called synthetic division is faster, with less writing and fewer calculations, especially when the divisor is a linear polynomial. 
Polynomial long division is possible provided that the coefficients of the polynomials belong to the same field, meaning that division by nonzero elements is always possible; examples of fields include the rational numbers, real numbers, and complex numbers.


== Example ==
Find the quotient and the remainder of the division of  
  
    
      
        (
        
          x
          
            3
          
        
        −
        2
        
          x
          
            2
          
        
        −
        4
        )
      
    
    {\\displaystyle (x^{3}-2x^{2}-4)}
  
, the dividend, by 
  
    
      
        (
        x
        −
        3
        )
      
    
    {\\displaystyle (x-3)}
  
, the divisor.
The dividend is first rewritten like this:

  
    
      
        
          x
          
            3
          
        
        −
        2
        
          x
          
            2
          
        
        +
        0
        x
        −
        4.
      
    
    {\\displaystyle x^{3}-2x^{2}+0x-4.}
  

The quotient and remainder can then be determined as follows:

Divide the first term of the dividend by the highest term of the divisor (meaning the one with the highest power of x, which in this case is x). Place the result above the bar: 
  
    
      
        
          x
          
            3
          
        
        ÷
        x
        =
        
          x
          
            2
          
        
      
    
    {\\displaystyle x^{3}\\div x=x^{2}}
  
.

  
    
      
        
          
            
              
                
                  
                    x
                    −
                    3
                     
                    )
                     
                    
                      x
                      
                        3
                      
                    
                    −
                    2
                  
                
                
                  x
                  
                    2
                  
                
              
            
            
              
                x
                −
                3
                 
                
                  
                    
                      )
                       
                      
                        x
                        
                          3
                        
                      
                      −
                      2
                      
                        x
                        
                          2
                        
                      
                      +
                      0
                      x
                      −
                      4
                    
                    ¯
                  
                
              
            
          
        
      
    
    {\\displaystyle {\\begin{array}{l}{\\color {White}x-3\\ )\\ x^{3}-2}x^{2}\\\\x-3\\ {\\overline {)\\ x^{3}-2x^{2}+0x-4}}\\end{array}}}
  

Multiply the divisor by the result just obtained (the first term of the eventual quotient). Write the result under the first two terms of the dividend: 
  
    
      
        
          x
          
            2
          
        
        ⋅
        (
        x
        −
        3
        )
        =
        
          x
          
            3
          
        
        −
        3
        
          x
          
            2
          
        
      
    
    {\\displaystyle x^{2}\\cdot (x-3)=x^{3}-3x^{2}}
  
.

  
    
      
        
          
            
              
                
                  
                    x
                    −
                    3
                     
                    )
                     
                    
                      x
                      
                        3
                      
                    
                    −
                    2
                  
                
                
                  x
                  
                    2
                  
                
              
            
            
              
                x
                −
                3
                 
                
                  
                    
                      )
                       
                      
                        x
                        
                          3
                        
                      
                      −
                      2
                      
                        x
                        
                          2
                        
                      
                      +
                      0
                      x
                      −
                      4
                    
                    ¯
                  
                
              
            
            
              
                
                  
                    x
                    −
                    3
                     
                    )
                     
                  
                
                
                  x
                  
                    3
                  
                
                −
                3
                
                  x
                  
                    2
                  
                
              
            
          
        
      
    
    {\\displaystyle {\\begin{array}{l}{\\color {White}x-3\\ )\\ x^{3}-2}x^{2}\\\\x-3\\ {\\overline {)\\ x^{3}-2x^{2}+0x-4}}\\\\{\\color {White}x-3\\ )\\ }x^{3}-3x^{2}\\end{array}}}
  

Subtract the product just obtained from the appropriate terms of the original dividend (being careful that subtracting something having a minus sign is equivalent to adding something having a plus sign), and write the result underneath 
  
    
      
        
          (
          
            
              x
              
                3
              
            
            −
            2
            
              x
              
                2
              
            
          
          )
        
        −
        
          (
          
            
              x
              
                3
              
            
            −
            3
            
              x
              
                2
              
            
          
          )
        
        =
        −
        2
        
          x
          
            2
          
        
        +
        3
        
          x
          
            2
          
        
        =
        
          x
          
            2
          
        
      
    
    {\\displaystyle \\left(x^{3}-2x^{2}\\right)-\\left(x^{3}-3x^{2}\\right)=-2x^{2}+3x^{2}=x^{2}}
  
.""",
    tier=6,
    domain="algebra",
    source="Wikipedia, 'Polynomial long division'",
    source_url="https://en.wikipedia.org/wiki/Polynomial_long_division",
))

register_atom(Atom(
    atom_type="definition",
    name="set_operations",
    content="""In combinatorics, the inclusion–exclusion principle is a counting technique which generalizes the familiar method of obtaining the number of elements in the union of two finite sets; symbolically expressed as

  
    
      
        
          |
        
        A
        ∪
        B
        
          |
        
        =
        
          |
        
        A
        
          |
        
        +
        
          |
        
        B
        
          |
        
        −
        
          |
        
        A
        ∩
        B
        
          |
        
      
    
    {\\displaystyle |A\\cup B|=|A|+|B|-|A\\cap B|}
  

where A and B are two finite sets and |S| indicates the cardinality of a set S (which may be considered as the number of elements of the set, if the set is finite). The formula expresses the fact that the sum of the sizes of the two sets may be too large since some elements may be counted twice. The double-counted elements are those in the intersection of the two sets and the count is corrected by subtracting the size of the intersection.
The inclusion-exclusion principle, being a generalization of the two-set case, is perhaps more clearly seen in the case of three sets, which for the sets A, B and C is given by 

  
    
      
        
          |
        
        A
        ∪
        B
        ∪
        C
        
          |
        
        =
        
          |
        
        A
        
          |
        
        +
        
          |
        
        B
        
          |
        
        +
        
          |
        
        C
        
          |
        
        −
        
          |
        
        A
        ∩
        B
        
          |
        
        −
        
          |
        
        A
        ∩
        C
        
          |
        
        −
        
          |
        
        B
        ∩
        C
        
          |
        
        +
        
          |
        
        A
        ∩
        B
        ∩
        C
        
          |
        
      
    
    {\\displaystyle |A\\cup B\\cup C|=|A|+|B|+|C|-|A\\cap B|-|A\\cap C|-|B\\cap C|+|A\\cap B\\cap C|}
  

This formula can be verified by counting how many times each region in the Venn diagram figure is included in the right-hand side of the formula. In this case, when removing the contributions of over-counted elements, the number of elements in the mutual intersection of the three sets has been subtracted too often, so must be added back in to get the correct total.

Generalizing the results of these examples gives the principle of inclusion–exclusion.  To find the cardinality of the union of n sets:

Include the cardinalities of the sets.
Exclude the cardinalities of the pairwise intersections.
Include the cardinalities of the triple-wise intersections.
Exclude the cardinalities of the quadruple-wise intersections.
Include the cardinalities of the quintuple-wise intersections.
Continue, until the cardinality of the n-tuple-wise intersection is included (if n is odd) or excluded (n even).
The name comes from the idea that the principle is based on over-generous inclusion, followed by compensating exclusion.
This concept is attributed to Abraham de Moivre (1718), although it first appears in a paper of Daniel da Silva (1854) and later in a paper by J. J. Sylvester (1883). Sometimes the principle is referred to as the formula of Da Silva or Sylvester, due to these publications. The principle can be viewed as an example of the sieve method extensively used in number theory and is sometimes referred to as the sieve formula.
As finite probabilities are computed as counts relative to the cardinality of the probability space, the formulas for the principle of inclusion–exclusion remain valid when the cardinalities of the sets are replaced by finite probabilities. More generally, both versions of the principle can be put under the common umbrella of measure theory.
In a very abstract setting, the principle of inclusion–exclusion can be expressed as the calculation of the inverse of a certain matrix. This inverse has a special structure, making the principle an extremely valuable technique in combinatorics and related areas of mathematics. As Gian-Carlo Rota put it:

"One of the most useful principles of enumeration in discrete probability and combinatorial theory is the celebrated principle of inclusion–exclusion.""",
    tier=3,
    domain="set_theory",
    source="Wikipedia, 'Inclusion–exclusion principle'",
    source_url="https://en.wikipedia.org/wiki/Inclusion%E2%80%93exclusion_principle",
))

register_atom(Atom(
    atom_type="definition",
    name="vigenere",
    content="""The Vigenère cipher (French pronunciation: [viʒnɛːʁ]) is a method of encrypting alphabetic text where each letter of the plaintext is encoded with a different Caesar cipher, whose increment is determined by the corresponding letter of another text, the key. In a Caesar cipher, each letter of the alphabet is shifted along some number of places. In a Caesar cipher of shift 3, a would become D, b would become E, y would become B and so on. The Vigenère cipher has several Caesar ciphers in sequence with different shift values.
For example, if the plaintext is attacking tonight and the key is oculorhinolaryngology, then

the first letter of the plaintext, a, is shifted by 14 positions in the alphabet (because the first letter of the key, o, is the 14th letter of the alphabet, counting from zero), yielding o;
the second letter, t, is shifted by 2 (because the second letter of the key, c, is the 2nd letter of the alphabet, counting from zero) yielding v;
the third letter, t, is shifted by 20 (u), yielding n, with wrap-around;
and so on.  
Traditionally spaces and punctuation are removed prior to encryption and reintroduced afterwards. 

In this example the tenth letter of the plaintext t is shifted by 14 positions (because the tenth letter of the key o is the 14th letter of the alphabet, counting from zero). Therefore, the encryption yields the message ovnlqbpvt hznzeuz.
If the recipient of the message knows the key, they can recover the plaintext by reversing this process.
The Vigenère cipher is therefore a special case of a polyalphabetic substitution.
First described by Giovan Battista Bellaso in 1553, the cipher is easy to understand and implement, but it resisted all attempts to break it until 1863, three centuries later. This earned it the description le chiffrage indéchiffrable (French for 'the indecipherable cipher').  Many people have tried to implement encryption schemes that are essentially Vigenère ciphers. In 1863, Friedrich Kasiski was the first to publish a general method of deciphering Vigenère ciphers.
In the 19th century, the scheme was misattributed to Blaise de Vigenère (1523–1596) and so acquired its present name.


== History ==
The very first well-documented description of a polyalphabetic cipher was by Leon Battista Alberti around 1467 and used a metal cipher disk to switch between cipher alphabets. Alberti's system only switched alphabets after several words, and switches were indicated by writing the letter of the corresponding alphabet in the ciphertext. Later, Johannes Trithemius, in his work Polygraphia (which was completed in manuscript form in 1508 but first published in 1518), invented the tabula recta, a critical component of the Vigenère cipher. The Trithemius cipher, however, provided a progressive, rather rigid and predictable system for switching between cipher alphabets.
In 1586 Blaise de Vigenère published a type of polyalphabetic cipher called an autokey cipher – because its key is based on the original plaintext – before the court of Henry III of France. The cipher now known as the Vigenère cipher, however, is based on that originally described by Giovan Battista Bellaso in his 1553 book La cifra del Sig. Giovan Battista Bellaso. He built upon the tabula recta of Trithemius but added a repeating "countersign" (a key) to switch cipher alphabets every letter.
Whereas Alberti and Trithemius used a fixed pattern of substitutions, Bellaso's scheme meant the pattern of substitutions could be easily changed, simply by selecting a new key. Keys were typically single words or short phrases, known to both parties in advance, or transmitted "out of band" along with the message, Bellaso's method thus required strong security for only the key. As it is relatively easy to secure a short key phrase, such as by a previous private conversation, Bellaso's system was considerably more secure.
However, as opposed to the modern Vigenère cipher, Bellaso's cipher did not have 26 different "shifts" (different Caesar's ciphers) for every letter, instead having 13 shifts for pairs of letters. In the 19th century, the invention of this cipher, essentially designed by Bellaso, was misattributed to Vigenère. David Kahn, in his book The Codebreakers, lamented this misattribution, saying that history had "ignored this important contribution and instead named a regressive and elementary cipher for him [Vigenère] though he had nothing to do with it".
The Vigenère cipher gained a reputation for being exceptionally strong. Noted author and mathematician Charles Lutwidge Dodgson (Lewis Carroll) called the Vigenère cipher unbreakable in his 1868 piece "The Alphabet Cipher" in a children's magazine. In 1917, Scientific American described the Vigenère cipher as "impossible of translation". That reputation was not deserved. Charles Babbage is known to have broken a variant of the cipher as early as 1854 but did not publish his work. One hypothesis is that he intentionally kept the general method secret, since he was a cryptographical adviser to his friend, Rear-Admiral Sir Francis Beaufort, during the Crimean War. Kasiski entirely broke the cipher and published the technique in the 19th century, but even in the 16th century, some skilled cryptanalysts could occasionally break the cipher.

The Vigenère cipher is simple enough to be a field cipher if it is used in conjunction with cipher disks. The Confederate States of America, for example, used a brass cipher disk to implement the Vigenère cipher during the American Civil War. The Confederacy's messages were far from secret, and the Union regularly cracked its messages. Throughout the war, the Confederate leadership primarily relied upon three key phrases: "Manchester Bluff", "Complete Victory" and, as the war came to a close, "Come Retribution".
A Vigenère cipher with a completely random (and non-reusable) key which is as long as the message becomes a one-time pad, a theoretically unbreakable cipher. Gilbert Vernam tried to repair the broken cipher (creating the Vernam–Vigenère cipher in 1918), but the technology he used was so cumbersome as to be impracticable.


== Tabula recta ==

For a visual way to encrypt and decrypt text, a table of alphabets can be used. The tabula recta, Vigenère square, or Vigenère table has the alphabet written out 26 times in different rows, with each alphabet shifted cyclically to the left compared to the previous alphabet, corresponding to the 26 possible Caesar ciphers. 
For example, suppose that the plaintext to be encrypted is

helloworld
And the example keyword is "key" and is repeated until it matches the length of the plaintext 

keykeykeyk
In order to encrypt the first letter of the plaintext using the tabula recta, go to column (H) and find where it meets with row (K). "R" is the result. After doing this repeatedly for each letter, the full plaintext can be encrypted 

rijvsuyvjn
To decrypt, go to the column for the key letter (K) and find the ciphertext letter (R) within it. The row in which (R) appears is headed by (H), which is the decrypted plaintext letter.


== Algebraic description ==
Vigenère can also be described algebraically.""",
    tier=5,
    domain="cryptography",
    source="Wikipedia, 'Vigenère cipher'",
    source_url="https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher",
))

register_atom(Atom(
    atom_type="definition",
    name="diophantine",
    content="""In mathematics, Bézout's identity (also called Bézout's lemma), named after Étienne Bézout who proved it for polynomials, is a theorem which relates two arbitrary integers with their greatest common divisor. The theorem's statement is as follows:

(The greatest common divisor of 0 and 0 is taken to be 0.) The integers x and y are called Bézout coefficients for (a, b); they are not unique. The extended Euclidean algorithm can be used to compute a minimal pair of Bézout coefficients, meaning they satisfy 
  
    
      
        
          |
        
        x
        
          |
        
        ≤
        
          |
        
        b
        
          /
        
        d
        
          |
        
      
    
    {\\displaystyle |x|\\leq |b/d|}
  
 and 
  
    
      
        
          |
        
        y
        
          |
        
        <
        
          |
        
        a
        
          /
        
        d
        
          |
        
      
    
    {\\displaystyle |y|<|a/d|}
  
; equality occurs only if one of a and b is a multiple of the other, and otherwise there exist exactly two minimal pairs.
As an example, the greatest common divisor of 
  
    
      
        a
        =
        15
      
    
    {\\displaystyle a=15}
  
 and 
  
    
      
        b
        =
        69
      
    
    {\\displaystyle b=69}
  
 is 
  
    
      
        d
        =
        3
      
    
    {\\displaystyle d=3}
  
, which can be written as the linear combination 
  
    
      
        a
        x
        +
        b
        y
        =
        15
        (
        −
        9
        )
        +
        69
        (
        2
        )
        =
        3
      
    
    {\\displaystyle ax+by=15(-9)+69(2)=3}
  
 with Bézout coefficients 
  
    
      
        (
        x
        ,
        y
        )
        =
        (
        −
        9
        ,
        2
        )
      
    
    {\\displaystyle (x,y)=(-9,2)}
  
, which are minimal since 
  
    
      
        9
        <
        69
        
          /
        
        3
        =
        23
      
    
    {\\displaystyle 9<69/3=23}
  
 and 
  
    
      
        2
        <
        15
        
          /
        
        3
        =
        5
      
    
    {\\displaystyle 2<15/3=5}
  
. The other minimal Bézout coefficients are 
  
    
      
        (
        x
        ,
        y
        )
        =
        (
        −
        9
        +
        23
        ,
        2
        −
        5
        )
        =
        (
        14
        ,
        −
        3
        )
      
    
    {\\displaystyle (x,y)=(-9+23,2-5)=(14,-3)}
  
.
Many other theorems in elementary number theory, such as  Euclid's lemma or the Chinese remainder theorem, can be formally deduced from Bézout's identity.
A Bézout domain is an integral domain in which Bézout's identity holds. In particular, Bézout's identity holds in principal ideal domains. Every theorem that results from Bézout's identity is thus true in all principal ideal domains.


== Structure of solutions ==
If a and b are not both zero and one pair of Bézout coefficients (x, y) has been computed (for example, using the extended Euclidean algorithm), all pairs can be represented in the form

  
    
      
        
          (
          
            x
            −
            k
            
              
                b
                d
              
            
            ,
             
            y
            +
            k
            
              
                a
                d
              
            
          
          )
        
        ,
      
    
    {\\displaystyle \\left(x-k{\\frac {b}{d}},\\ y+k{\\frac {a}{d}}\\right),}
  

where k is an arbitrary integer, d is the greatest common divisor of a and b, and the fractions simplify to integers.
If a and b are both nonzero and none of them divides the other, then exactly two of the pairs of Bézout coefficients satisfy 

  
    
      
        
          |
        
        x
        
          |
        
        <
        
          |
          
            
              b
              d
            
          
          |
        
        
        
          and
        
        
        
          |
        
        y
        
          |
        
        <
        
          |
          
            
              a
              d
            
          
          |
        
        .
      
    
    {\\displaystyle |x|<\\left|{\\frac {b}{d}}\\right|\\quad {\\text{and}}\\quad |y|<\\left|{\\frac {a}{d}}\\right|.}
  
 If a and b are both positive, one has 
  
    
      
        x
        >
        0
      
    
    {\\displaystyle x>0}
  
 and 
  
    
      
        y
        <
        0
      
    
    {\\displaystyle y<0}
  
 for one of these pairs, and 
  
    
      
        x
        <
        0
      
    
    {\\displaystyle x<0}
  
 and 
  
    
      
        y
        >
        0
      
    
    {\\displaystyle y>0}
  
 for the other. If a > 0 is a divisor of b (including the case 
  
    
      
        b
        =
        0
      
    
    {\\displaystyle b=0}
  
), then one pair of Bézout coefficients is (1, 0).
This relies on a property of Euclidean division: given two non-zero integers c and d, if d does not divide c, there is exactly one pair (q, r) such that c = dq + r and 0 < r < |d|, and another one such that c = dq + r and −|d| < r < 0.
The two pairs of minimal Bézout coefficients are obtained from the given one (x, y) by choosing for k in the above formula either of the two integers nearest to ⁠x/b/d⁠.
The extended Euclidean algorithm always produces one of these two minimal pairs.


=== Example ===
Let a = 12 and b = 42, then gcd (12, 42) = 6.""",
    tier=6,
    domain="number_theory",
    source="Wikipedia, 'Bézout's identity'",
    source_url="https://en.wikipedia.org/wiki/B%C3%A9zout%27s_identity",
))
