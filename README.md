<h1>Learnings Bot</h1>

<h2>A telegram bot dedicated to tracking learnings/reflections</h2>
Ultimately, there's one investment that supersedes all others: Invest in yourself. This quote by Warren Buffet is something which a couple of us strongly believed in, and thus we created a group with the shared goal of making at least an hour of deliberate learning effort every single day. We motivate and learn from each other by keeping each other accountable, and this bot is designed to do just that.

We had a mini-game to see who can create the better bot, and you can find the bots by the rest of the warriors here: 
<ul>
 <li><a href ="https://github.com/tingzhouu/habit-telegram-bot#habit-telegram-bot">Ting Zhou </a></li>
 <li><a href ="https://github.com/Suman-Vanan/deliberate-practice-telegram-bot">Suman Vanan</a></li>
  <li><a href ="https://github.com/weekian/telegram-log-bot">Wee Kian</a></li>
 </ul>


<h2>Technology Used</h2> 
<ul>
  <li><bold>Python</bold> is used for the backend application logic</li>
  <li><bold>SQLite</bold> is used for the database of the application</li>
  <li><bold>Python Anywhere</bold>is used for lightweight hosting of the application</li>
</ul>


<h2>Files</h2> 

<h3>Todo.py</h3> 
This file contains the main logic needed for the bot to send/receive messages. For more information on how the logic works, you can refer to <a href="https://core.telegram.org/bots/api">Telegrams api.</a>

<h3>Commands.py</h3>
This file contains the logic flow for deciding which sequence of logic to execute when the user makes a command. Currently, the only supported commands as of version 1.0 are: /checkin, /checkout, /summary.

<ul>
  <li><bold>/Checkin:</bold> Takes note of what time the user starts clocking their time. </li>
  <li><bold>/Checkout:</bold> Takes note of what time the user clocks out their time, along with what they have done for their check-in session. The activities and the difference in duration is displayed and stored into the database. </li>
  <li><bold>/Summary:</bold> Retrieves all checked-in activities by all users for the day.</li>
</ul> 

<h2>Upcoming features</h2> 
  
<ul>
  <li>Cheat day feature to get 1 day off </li>
  <li>Penalty feature to calculate penalties incurred for skipping daily learnings</li>
  <li>CI/CD pipeline via Heroku</li> 
  <li>Better formatting of messages</li> 
  <li>Unit tests</li>
  <li>Check-out validation: Unable to check-out without logging an activity</li> 
  <li>Summary to allow retrieval of individual/group activities of past dates</li> 
</ul> 

<h2>Ending</h2>

This bot is created by Tan Chong Yong. You can follow me on my blog to read about my learnings and thoughts of things that interest me, particulary tech,investment and startup related stuff.

