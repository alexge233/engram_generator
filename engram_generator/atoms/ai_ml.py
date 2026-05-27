"""AI/ML knowledge atoms sourced from Wikipedia."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom

register_atom(Atom(
    atom_type="algorithm",
    name="gradient_descent",
    content="""Gradient descent is a method for unconstrained mathematical optimization. It is a first-order iterative algorithm for minimizing a differentiable multivariate function. The idea is to take repeated steps in the opposite direction of the gradient (or approximate gradient) of the function at the current point, because this is the direction of steepest descent. Conversely, stepping in the direction of the gradient will lead to a trajectory that maximizes that function; the procedure is then known as gradient ascent. Gradient descent is particularly useful in machine learning and artificial intelligence for minimizing the cost or loss function. Gradient descent is generally attributed to Augustin-Louis Cauchy, who first suggested it in 1847. Jacques Hadamard independently proposed a similar method in 1907. Its convergence properties for non-linear optimization problems were first studied by Haskell Curry in 1944, with the method becoming increasingly well-studied and used in the following decades.""",
    tier=4,
    domain="optimization",
    source="Wikipedia, 'Gradient descent'",
    source_url="https://en.wikipedia.org/wiki/Gradient_descent",
    prerequisites=["derivative_eval"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="momentum_sgd",
    content="""Stochastic gradient descent (often abbreviated SGD) is an iterative method for optimizing an objective function with suitable smoothness properties (e.g. differentiable or subdifferentiable). It can be regarded as a stochastic approximation of gradient descent optimization, since it replaces the actual gradient (calculated from the entire data set) by an estimate thereof (calculated from a randomly selected subset of the data). Especially in high-dimensional optimization problems this reduces the very high computational burden, achieving faster iterations in exchange for a lower convergence rate. The basic idea behind stochastic approximation can be traced back to the Robbins-Monro algorithm of the 1950s. Today, stochastic gradient descent has become an important optimization method in machine learning. Momentum SGD extends basic SGD by accumulating a velocity vector v = beta*v + gradient, then updating weights w = w - lr*v. This dampens oscillations and accelerates convergence along consistent gradient directions.""",
    tier=5,
    domain="optimization",
    source="Wikipedia, 'Stochastic gradient descent'",
    source_url="https://en.wikipedia.org/wiki/Stochastic_gradient_descent",
    prerequisites=["gradient_descent"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="adam_optimizer",
    content="""Adam (Adaptive Moment Estimation) is an optimization algorithm used as an alternative to classical stochastic gradient descent to update network weights during training. Adam combines the advantages of two other extensions of SGD: AdaGrad, which adapts the learning rate to parameters, and RMSProp, which also uses an exponentially decaying average of squared gradients. Adam maintains per-parameter learning rates that are adapted based on first moment (mean) and second moment (uncentered variance) estimates of the gradients. The update rules are: m_t = beta1*m_{t-1} + (1-beta1)*g_t, v_t = beta2*v_{t-1} + (1-beta2)*g_t^2, followed by bias correction m_hat = m_t/(1-beta1^t), v_hat = v_t/(1-beta2^t), and weight update w = w - lr*m_hat/(sqrt(v_hat)+eps). Default hyperparameters are beta1=0.9, beta2=0.999, eps=1e-8. Adam was proposed by Diederik P. Kingma and Jimmy Ba in their 2014 paper.""",
    tier=5,
    domain="optimization",
    source="Wikipedia, 'Stochastic gradient descent'",
    source_url="https://en.wikipedia.org/wiki/Stochastic_gradient_descent",
    prerequisites=["momentum_sgd"],
))

register_atom(Atom(
    atom_type="formula",
    name="learning_rate_decay",
    content="""In machine learning and statistics, the learning rate is a tuning parameter in an optimization algorithm that determines the step size at each iteration while moving toward a minimum of a loss function. Since it influences to what extent newly acquired information overrides old information, it metaphorically represents the speed at which a machine learning model "learns". In the adaptive control literature, the learning rate is commonly referred to as gain. In setting a learning rate, there is a trade-off between the rate of convergence and overshooting. While the descent direction is usually determined from the gradient of the loss function, the learning rate determines how big a step is taken in that direction. Too high a learning rate will make the learning jump over minima, but too low a learning rate will either take too long to converge or get stuck in an undesirable local minimum. In order to achieve faster convergence, prevent oscillations and getting stuck in undesirable local minima the learning rate is often varied during training either in accordance to a learning rate schedule or by using an adaptive learning rate.""",
    tier=4,
    domain="optimization",
    source="Wikipedia, 'Learning rate'",
    source_url="https://en.wikipedia.org/wiki/Learning_rate",
    prerequisites=["exponentiation", "multiplication"],
))

register_atom(Atom(
    atom_type="formula",
    name="mean_squared_error",
    content="""In statistics, the mean squared error (MSE) or mean squared deviation (MSD) of an estimator (of a procedure for estimating an unobserved quantity) measures the average of the squares of the errors -- that is, the average squared difference between the estimated values and the true value. MSE is a risk function, corresponding to the expected value of the squared error loss. The fact that MSE is almost always strictly positive (and not zero) is because of randomness or because the estimator does not account for information that could produce a more accurate estimate. In machine learning, specifically empirical risk minimization, MSE may refer to the empirical risk (the average loss on an observed data set), as an estimate of the true MSE (the true risk: the average loss on the actual population distribution). The MSE is a measure of the quality of an estimator. As it is derived from the square of Euclidean distance, it is always a positive value that decreases as the error approaches zero.""",
    tier=4,
    domain="loss_functions",
    source="Wikipedia, 'Mean squared error'",
    source_url="https://en.wikipedia.org/wiki/Mean_squared_error",
    prerequisites=["mean", "exponentiation"],
))

register_atom(Atom(
    atom_type="formula",
    name="binary_cross_entropy",
    content="""In information theory, cross-entropy between two probability distributions p and q measures the average number of bits needed to identify an event drawn from the set when the coding scheme used for the set is optimized for an estimated probability distribution q, rather than the true distribution p. Binary cross-entropy is the special case for two classes: BCE = -[y*log(p) + (1-y)*log(1-p)], where y is the true binary label (0 or 1) and p is the predicted probability. It is the standard loss function for binary classification problems in neural networks. Minimizing BCE is equivalent to maximizing the likelihood of the correct class under a Bernoulli distribution. The gradient of BCE with respect to the predicted probability p is (p-y)/(p*(1-p)), which provides a strong learning signal when predictions are confident but wrong.""",
    tier=5,
    domain="loss_functions",
    source="Wikipedia, 'Cross-entropy'",
    source_url="https://en.wikipedia.org/wiki/Cross-entropy",
    prerequisites=["cross_entropy"],
))

register_atom(Atom(
    atom_type="formula",
    name="kl_divergence",
    content="""In mathematical statistics, the Kullback-Leibler (KL) divergence (also called relative entropy and I-divergence), denoted D_KL(P||Q), is a type of statistical distance: a measure of how much an approximating probability distribution Q is different from a true probability distribution P. Mathematically, it is defined as D_KL(P||Q) = sum_{x in X} P(x) log(P(x)/Q(x)). KL divergence is not symmetric: D_KL(P||Q) != D_KL(Q||P) in general. It is always non-negative (Gibbs' inequality), and equals zero if and only if P = Q almost everywhere. KL divergence is widely used in machine learning for variational inference, knowledge distillation, and regularising generative models. It measures the extra bits needed to encode samples from P using a code optimised for Q.""",
    tier=5,
    domain="information_theory",
    source="Wikipedia, 'Kullback-Leibler divergence'",
    source_url="https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence",
    prerequisites=["info_entropy"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="batch_normalization",
    content="""In artificial neural networks, batch normalization (also known as batch norm) is a normalization technique used to make training faster and more stable by adjusting the inputs to each layer -- re-centering them around zero and re-scaling them to a standard size. It was introduced by Sergey Ioffe and Christian Szegedy in 2015. Experts still debate why batch normalization works so well. It was initially thought to tackle internal covariate shift, a problem where parameter initialization and changes in the distribution of the inputs of each layer affect the learning rate of the network. However, newer research suggests it doesn't fix this shift but instead smooths the objective function -- a mathematical guide the network follows to improve -- enhancing performance. In very deep networks, batch normalization can initially cause a severe gradient explosion -- where updates to the network grow uncontrollably large -- but this is managed with shortcuts called skip connections in residual networks.""",
    tier=5,
    domain="neural_networks",
    source="Wikipedia, 'Batch normalization'",
    source_url="https://en.wikipedia.org/wiki/Batch_normalization",
    prerequisites=["mean", "variance"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="dropout",
    content="""Dropout and dilution (also called DropConnect) are regularization techniques for reducing overfitting in artificial neural networks by preventing complex co-adaptations on training data. They are an efficient way of performing model averaging with neural networks. Dilution refers to randomly decreasing weights towards zero, while dropout refers to randomly setting the outputs of hidden neurons to zero. Both are usually performed during the training process of a neural network, not during inference. During training, dropout randomly zeroes elements of the input tensor with probability p using samples from a Bernoulli distribution. Each channel will be zeroed out independently on every forward call. The outputs are scaled by 1/(1-p) during training so that the expected value of each neuron's output remains the same at test time. This inverted dropout approach avoids the need to modify the network at inference time.""",
    tier=5,
    domain="neural_networks",
    source="Wikipedia, 'Dilution (neural networks)'",
    source_url="https://en.wikipedia.org/wiki/Dilution_(neural_networks)",
    prerequisites=["multiplication", "division"],
))

register_atom(Atom(
    atom_type="formula",
    name="conv_output_size",
    content="""A convolutional neural network (CNN) is a type of feedforward neural network that learns features via filter (or kernel) optimization. The output spatial dimension of a convolution layer is determined by the formula O = (W - K + 2P) / S + 1, where W is the input width (or height), K is the kernel size, P is the padding, and S is the stride. This formula applies independently to each spatial dimension. When the result is not an integer, the convolution is invalid for those parameters (some frameworks floor the result). Vanishing gradients and exploding gradients, seen during backpropagation in earlier neural networks, are prevented by the regularization that comes from using shared weights over fewer connections. Higher-layer features are extracted from wider context windows, compared to lower-layer features.""",
    tier=4,
    domain="neural_networks",
    source="Wikipedia, 'Convolutional neural network'",
    source_url="https://en.wikipedia.org/wiki/Convolutional_neural_network",
    prerequisites=["division", "addition"],
))

register_atom(Atom(
    atom_type="formula",
    name="bellman_equation",
    content="""A Bellman equation, named after Richard E. Bellman, is a technique in dynamic programming which breaks an optimization problem into a sequence of simpler subproblems, as Bellman's "principle of optimality" prescribes. It is a necessary condition for optimality. The "value" of a decision problem at a certain point in time is written in terms of the payoff from some initial choices and the "value" of the remaining decision problem that results from those initial choices. The equation applies to algebraic structures with a total ordering; for algebraic structures with a partial ordering, the generic Bellman's equation can be used. The Bellman equation was first applied to engineering control theory and to other topics in applied mathematics, and subsequently became an important tool in economic theory. In reinforcement learning, the Bellman equation relates the value of a state to the expected reward plus the discounted value of successor states: V(s) = R(s) + gamma * max_a sum P(s'|s,a) V(s').""",
    tier=6,
    domain="reinforcement_learning",
    source="Wikipedia, 'Bellman equation'",
    source_url="https://en.wikipedia.org/wiki/Bellman_equation",
    prerequisites=["expected_value", "multiplication"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="q_learning",
    content="""Q-learning is a reinforcement learning algorithm that trains an agent to assign values to its possible actions based on its current state, without requiring a model of the environment (model-free). It can handle problems with stochastic transitions and rewards without requiring adaptations. For any finite Markov decision process, Q-learning finds an optimal policy in the sense of maximizing the expected value of the total reward over any and all successive steps, starting from the current state. Q-learning can identify an optimal action-selection policy for any given finite Markov decision process, given infinite exploration time and a partly random policy. "Q" refers to the function that the algorithm computes: the expected reward -- that is, the quality -- of an action taken in a given state. The TD update rule is Q(s,a) = Q(s,a) + alpha*(R + gamma*max_a' Q(s',a') - Q(s,a)).""",
    tier=6,
    domain="reinforcement_learning",
    source="Wikipedia, 'Q-learning'",
    source_url="https://en.wikipedia.org/wiki/Q-learning",
    prerequisites=["bellman_equation"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="policy_gradient",
    content="""Policy gradient methods are a class of reinforcement learning algorithms that optimize a parameterized policy directly by estimating the gradient of expected cumulative reward with respect to the policy parameters. The REINFORCE algorithm, proposed by Ronald J. Williams in 1992, is the foundational policy gradient method. It uses the log-likelihood ratio trick: the gradient of the expected reward J(theta) is estimated as E[nabla log pi(a|s; theta) * R], where pi(a|s; theta) is the probability of taking action a in state s under policy parameters theta, and R is the observed return. Variance reduction is typically achieved through a baseline subtraction: replacing R with the advantage A = R - b, where b is a learned value function baseline. Policy gradient methods can handle continuous action spaces and stochastic policies naturally, unlike value-based methods.""",
    tier=6,
    domain="reinforcement_learning",
    source="Wikipedia, 'Reinforcement learning'",
    source_url="https://en.wikipedia.org/wiki/Reinforcement_learning",
    prerequisites=["backprop_simple"],
))

register_atom(Atom(
    atom_type="formula",
    name="mutual_information",
    content="""In probability theory and information theory, the mutual information (MI) of two random variables is a measure of the mutual dependence between the two variables. More specifically, it quantifies the "amount of information" obtained about one random variable by observing the other random variable. The concept of mutual information is intimately linked to that of entropy of a random variable, a fundamental notion in information theory that defines the "amount of information" held in a random variable. Not limited to real-valued random variables and linear dependence like the correlation coefficient, MI is more general and determines how different the joint distribution of the pair (X,Y) is from the product of the marginal distributions of X and Y. MI is defined as I(X;Y) = H(X) + H(Y) - H(X,Y), where H denotes Shannon entropy. It was formally introduced by Claude Shannon in his foundational information theory paper.""",
    tier=5,
    domain="information_theory",
    source="Wikipedia, 'Mutual information'",
    source_url="https://en.wikipedia.org/wiki/Mutual_information",
    prerequisites=["info_entropy"],
))

register_atom(Atom(
    atom_type="formula",
    name="kl_from_distributions",
    content="""In mathematical statistics, the Kullback-Leibler (KL) divergence (also called relative entropy and I-divergence), denoted D_KL(P||Q), is a type of statistical distance: a measure of how much an approximating probability distribution Q is different from a true probability distribution P. Mathematically, it is defined as D_KL(P||Q) = sum_{x in X} P(x) log(P(x)/Q(x)). For discrete distributions, each term p_i * log(p_i/q_i) measures how much information is lost when q_i is used to approximate p_i. The KL divergence is asymmetric: D_KL(P||Q) measures the cost of using Q to approximate P, which differs from D_KL(Q||P). This asymmetry is important in variational inference where the choice of direction affects the approximation quality.""",
    tier=5,
    domain="information_theory",
    source="Wikipedia, 'Kullback-Leibler divergence'",
    source_url="https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence",
    prerequisites=["kl_divergence"],
))

register_atom(Atom(
    atom_type="formula",
    name="markov_reward",
    content="""A Markov decision process (MDP) is a mathematical model for sequential decision making when outcomes are uncertain. It is a type of stochastic decision process, and is often solved using the methods of stochastic dynamic programming. Originating from operations research in the 1950s, MDPs have since gained recognition in a variety of fields, including ecology, economics, healthcare, telecommunications and reinforcement learning. Reinforcement learning utilizes the MDP framework to model the interaction between a learning agent and its environment. In this framework, the interaction is characterized by states, actions, and rewards. The expected reward for a policy pi in state s is computed as E[R] = sum_a pi(a|s) * R(s,a), where pi(a|s) is the probability of taking action a in state s and R(s,a) is the reward for that state-action pair. The name comes from its connection to Markov chains, a concept developed by the Russian mathematician Andrey Markov.""",
    tier=5,
    domain="reinforcement_learning",
    source="Wikipedia, 'Markov decision process'",
    source_url="https://en.wikipedia.org/wiki/Markov_decision_process",
    prerequisites=["markov_chain", "expected_value"],
))

register_atom(Atom(
    atom_type="formula",
    name="discounted_return",
    content="""In reinforcement learning, the discounted return (also called discounted cumulative reward) at time step t is defined as G_t = R_t + gamma*R_{t+1} + gamma^2*R_{t+2} + ... = sum_{k=0}^{T} gamma^k * R_{t+k}, where gamma in [0,1] is the discount factor and R_{t+k} is the reward received k steps after time t. The discount factor gamma determines the present value of future rewards: a gamma close to 0 makes the agent short-sighted (only caring about immediate rewards), while a gamma close to 1 makes it far-sighted (valuing future rewards almost as much as immediate ones). The discounted return is central to the definition of value functions V(s) = E[G_t | S_t = s] and action-value functions Q(s,a) = E[G_t | S_t = s, A_t = a] in reinforcement learning.""",
    tier=5,
    domain="reinforcement_learning",
    source="Wikipedia, 'Markov decision process'",
    source_url="https://en.wikipedia.org/wiki/Markov_decision_process",
    prerequisites=["exponentiation", "prefix_scan"],
))

register_atom(Atom(
    atom_type="definition",
    name="confusion_matrix",
    content="""In machine learning, a confusion matrix, also known as error matrix, is a specific table layout that allows visualization of the performance of an algorithm, typically a supervised learning one. In unsupervised learning it is usually called a matching matrix. The term is used specifically in the problem of statistical classification. Each row of the matrix represents the instances in an actual class while each column represents the instances in a predicted class, or vice versa. The diagonal of the matrix therefore represents all instances that are correctly predicted. The name stems from the fact that it makes it easy to identify whether the system is confusing two classes (i.e., commonly mislabeling one class as another). From the confusion matrix, key metrics are derived: Precision = TP/(TP+FP), Recall = TP/(TP+FN), F1 = 2*Precision*Recall/(Precision+Recall). The confusion matrix has its origins in human perceptual studies of auditory stimuli.""",
    tier=4,
    domain="model_evaluation",
    source="Wikipedia, 'Confusion matrix'",
    source_url="https://en.wikipedia.org/wiki/Confusion_matrix",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="roc_auc",
    content="""A receiver operating characteristic curve, or ROC curve, is a graphical plot that illustrates the performance of a binary classifier model at varying threshold values. ROC analysis is commonly applied in the assessment of diagnostic test performance in clinical epidemiology. The ROC curve is the plot of the true positive rate (TPR) against the false positive rate (FPR) at each threshold setting. The ROC can also be thought of as a plot of the statistical power as a function of the Type I Error of the decision rule. The area under the ROC curve (AUC) provides an aggregate measure of performance across all possible classification thresholds. AUC ranges from 0 to 1, where 0.5 indicates random chance performance and 1.0 indicates perfect classification. AUC is computed using the trapezoidal rule: AUC = sum of trapezoids formed by consecutive (FPR, TPR) points.""",
    tier=5,
    domain="model_evaluation",
    source="Wikipedia, 'Receiver operating characteristic'",
    source_url="https://en.wikipedia.org/wiki/Receiver_operating_characteristic",
    prerequisites=["sorting", "confusion_matrix"],
))

register_atom(Atom(
    atom_type="principle",
    name="bias_variance_tradeoff",
    content="""In statistics and machine learning, the bias-variance tradeoff describes the relationship between a model's complexity, the accuracy of its predictions, and how well it can make predictions on previously unseen data that were not used to train the model. In general, as the number of tunable parameters in a model increases, it becomes more flexible, and can better fit a training data set. That is, the model has lower error or lower bias. However, for more flexible models, there will tend to be greater variance to the model fit each time we take a set of samples to create a new training data set. The bias-variance decomposition of mean squared error is: MSE = Bias^2 + Variance + irreducible noise. The bias error is an error from erroneous assumptions in the learning algorithm. High bias can cause an algorithm to miss the relevant relations between features and target outputs (underfitting). The variance is an error from sensitivity to small fluctuations in the training set. High variance may result from an algorithm modeling the random noise in the training data (overfitting).""",
    tier=5,
    domain="model_evaluation",
    source="Wikipedia, 'Bias-variance tradeoff'",
    source_url="https://en.wikipedia.org/wiki/Bias%E2%80%93variance_tradeoff",
    prerequisites=["mse_loss", "variance"],
))
