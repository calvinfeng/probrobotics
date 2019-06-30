# Taxonomy of Localization Problems

Not every localization problem is equally hard. 

## Local vs. Global

### Local

Position tracking assumes that the initial robot pose is known. Localizing the robot can be achieved by accommodating the noise in robot motion. The motion noise is usually small. The pose uncertainty is often approximated y a unimodal distribution, e.g. Gaussian again. The position tracking problem is a local problem, since the uncertainty is local and confined to region near the robot's true pose.

### Global

In global localization, the initial pose of the robot is unknown. The robot is initially placed somewhere in its environment, but it lacks knowledge of its whereabouts. Unimodal probability distributions are usually inappropriate to this problem. In general global localization is more difficult than position tracking.

### Kidnap

The kidnapped robot problem is a variant of the global localization problem, but one that is even more difficult. During operation, the robot can get kidnapped and teleported to some other location. The kidnapped robot problem is more difficult than the global localization problems, in that the robot might believe it knows where it is while it does not. 

## Static vs Dynamic Environments

### Static

Static environments are environments where the only variable quantity state is the robot's pose. All other objects in the environments remain at the same location forever. Static environments have some nice mathematical properties that make them amenable to efficient probabilistic estimation.

### Dynamic

Dynamic environment possesses objects other than the robot whose location or configuration changes over time. Of particular interest are changes that persist over time, and that impact more than a single sensor reading. Examples of more persistent changes are, people, move-able furniture, or doors.

## Passive vs. Active Approaches

### Passive

In passive localization, the localization module only observes the robot operating. The robot is controlled through some other means, and the robot's motion is not aimed at facilitating localization.

### Active

Active localization algorithms control the robot so as to minimize the localization error and the costs arising from moving a poorly localized robot into a hazardous place. 

## Single vs Multiple Robots

Single robot localization is the most commonly studied approach to localization. It deals with a single robot only. 

The multi-robot localization problem arises in teams of robots. At first glance, each robot could localize itself individually, hence the multi-robot problem can be solved through single robot approach. If the robots are able to detect each other, however, there is the opportunity to do better. This is because one robot's belief can be used to bias another robot's belief if knowledge of the relative location of both robots is available.

