<h1>Famile-Garbage_Classification</h1>
<p>A system built for family garbage classification</p>

<h3>System Introduction</h3>
<p> This system can serve as the management system to urge citizens to form a habit of garbage classification by raising rewards and penalties.</p>
<p> Every family or a room-scale group, like a dorm, should apply for accounts in the system.</p>
<p> Throwing garbage at the corresponding intelligent grabage collectors is the only valid way of throwing garbage.</p>
<p> Logging in is necessary as the premise of throwing garbage, after which user should pick mannually the type of garbage (3 types classified in our system). If success, the garbage will print and stick a unique QTcode on the garbage bag to link the user's information to the garbage.</p>
<p> We also design the schedule algorithm using greddy method based on the position of the car and the collectors (with the help of GPS) for garbage car to collect garbage from the collectors if the volumn of garbage reaches the threshold.</p>
<p> After the garbage is dumped from the car to the station, examination procedures are needed to check if the garbage is correctly classified by users. We implement this by AlexNet to recognize the objects in the picture of the garbage and classify the garbage based on the output of the AlexNet with the help of the word vector.</p>
<p> Still, the collector requirses to periodically send message to the hub to tell the hub that it is still in connection with the network. If the hub do not receive messages from some collectors, than repair men will be send to repair the collectors.</p>
<p> We design face-recognition system to trace the invalid behaviour of throwing, like throwing the garbage at somewhere else.</p>

<h3>Current Work</h3>
<p> We don't have the support of the hardware device, we can now demo it in the software level.</p>
<p> We use socket to implement the communication.</p>
<p> Our schedule algorithm is demo-ed under virtual 2-d space simulated in the computer.</p>

<h3>To Improve...</h3>
<p> If we have the dataset of the directed tag between garbage pictures and their type, our automatic examination algorithm will work much better.</p>
<p> Hardward support may be helpful in many senarios.</p>

<h3> Group Member</h3>
<ul type = "circle">
  <li><p><a href = 'https://github.com/wanwandebaba'>Tong Zhao</a></p></li>
  <li><p><a href = 'https://github.com/MarshalLeeeeee'>Minchao Li</a></p></li>
  <li><p><a href = 'https://github.com/374365283'>Chenfei Zhang</a></p></li>
  <li><p><a href = 'https://github.com/978326187'>Huachi Xu</a></p></li>
</ul>