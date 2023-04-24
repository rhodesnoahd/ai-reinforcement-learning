<div id="header" align="center">
  <h1> COSC 4368: FUNDAMENTALS OF ARTIFICIAL INTELLIGENCE
    <br><br>
   <img src="https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif" width="200"/>
   <img src="https://media.giphy.com/media/5k5vZwRFZR5aZeniqb/giphy.gif", width="200"/>
  </h1>
</div>
---

<h2>Team Name: Artificial Brilliance
  <ul><br>
    <li><b>Michael Moorman <img src="https://media.giphy.com/media/m0dmKBkncVETJv2h0S/giphy.gif" width="30px"/></b></li>
    <li><b>Abraar Patel &nbsp <img src="https://media.giphy.com/media/m0dmKBkncVETJv2h0S/giphy.gif" width="30px"/></b></li>
    <li><b>Noah Rhodes &nbsp<img src="https://media.giphy.com/media/m0dmKBkncVETJv2h0S/giphy.gif" width="30px"/></b></li>
  <li> <b>Gregory Flores-Blackburn &nbsp <img src="https://media.giphy.com/media/m0dmKBkncVETJv2h0S/giphy.gif" width="30px"/></b></li>
  </ul>
  </h2>
  
<h2> Description </h2>
 
 Using <b>reinforcement learning </b> to learn and adapt “promising paths” in 2-agent setting.<br>
 <br><b> LEARNING OBJECTIVES:</b>
 <ul>
 <li> Understanding basic reinforcement learning concepts such as utilities, policies, learning rates, discount rates and their interactions </li>
<li>	Obtain experience in designing agent-based systems that explore and learn in initially unknown environment and which are capable to adapt to changes </li> 
<li>	Learning how to conduct experiments that evaluate the performance of reinforcement learning systems and learning to interpret such results </li>
<li>	Development of visualization techniques summarizing how the agents move, how the world and the q-table changes, and the system performance</li>
<li>	Development of path visualization and analysis techniques to interpret and evaluate the behavior of agent-based path-learning systems </li>
<li>Develop and learn coordination strategies for collaborating agents</li>
<li>Creating solutions for 3D visualization problems</li>
<li>Learning to develop AI software in a team</li>
</ul>

<h2>How to run the code</h2>
<ol>
  <li>Install the dependencies in <i>requirements.txt</i>.
    <ul>
      <li>Example using <code>pip</code>: <code>pip install requirements.txt</code></li>
      <li>Example using <code>conda</code>: <code>conda install -c conda-forge numpy pygame pandas plotly==5.14.1</code></li>
    </ul>
  </li>
  <li>Simulate an experiment by running <i>main.py</i> with arguments. Required arguments are:
    <ul>
      <li>experiment</li>
      <li>seed</li>
    </ul>
    Acceptable experiment arguments are <code>1a</code>, <code>1b</code>, <code>1c</code>,<code>2</code>, <code>3a</code>, <code>3b</code> and <code>4</code>.
    Acceptable seed arguments include any integer greater than or equal to zero such as <code>42</code>.
    Optional arguments are:
    <ul>
      <li><code>--history</code> which writes history information to files used during offline visualization</li>
      <li><code>--dump-tables</code> which writes Q-table information to files used during offline visualization</li>
      <li><code>--rl</code> followed by any one of the following reinforcement learning state spaces <code>ss</code>, <code>vs</code>, <code>ms</code>. This selects the reinforcement learning state space used by the agents. If not provided, the default value is <code>ss</code>.</li>
      <li><code>--viz</code> followed by a destination for a <i>.csv</i> file. This file is used in <i>performanceMetrics.ipynb</i>. If not provided the default value is <code>out/visualization.csv</code></li>
    </ul>
  </li>
  <li>Visualize a simulated experiment by running <i>visualization.py</i>. <b>Note that you must run <i>main.py</i> beforehand with the optional <code>--history</code> flag in order to generate the files needed to run <i>visualization.py</i> without arguments. </b>You may optionally provide command line arguments when running <i>visualization.py</i>. Optional arguments are:
    <ul>
      <li><code>--fps</code> followed by an integer such as <code>30</code> to set the framerate of the display updates. If not provided, the default value is <code>60</code>.</li>
      <li><code>--qtable</code> followed by <code>F</code> or <code>M</code> which also visualizes the Q-table of corresponding agent. <b>Note that you must run <i>main.py</i> beforehand with the optional <code>--dump-tables</code> flag in order to produce the files needed to run <i>visualization.py</i> with this flag.</b></li>
      <li><code>--no-block</code> which, when provided, only displays Q-table information as if the agent is not carrying a block. This flag can't be provided if <code>--has-block</code> is also provided. This flag is intended to modify the contents generated when <code>--report</code> is provided.</li>
      <li><code>--has-block</code> which, when provided, only displays Q-table information as if the agent is carrying a block. This flag can't be provided if <code>--no-block</code> is also provided. This flag is intended to modify the contents generated when <code>--report</code> is provided.</li>
      <li><code>--report</code> which generates Q-table images at key moments in an experiment.</li>
      <li><code>--paused</code> which sets the visualization to begin in paused mode. You may take single steps with the right arrow key while paused, or toggle normal playback mode with the spacebar.</li>
    </ul>
  </li>
  <li>The performance variable data was aggregated for all experiments using the script <i>generate_csv.py</i>. This produces files <i>visualizationN.csv</i> and <i>terminal_statesN.csv</i> files in the <i>out</i> subdirectory. The Jupyter Notebook <i>performanceMetrics_visualization.ipynb</i> is used to generate the figure images in the report.
  </li>
</ol>
<h4>Example use after installing the dependencies </h4>

<p>
Consider the case where you wish to simulate experiment 1c with seed 2 and visualize it. To accomplish this, perform the following steps:
</p>
<ol>
  <li><code>python main.py 1a 2 --history</code></li>
  <li><code>python visualization.py</code></li>
</ol>

<p>
Consider the case where you wish to simulate experiment 4 with seed 39 and visualize it with agent M's Q-table information. Perhaps you also want to set the framerate to 30 fps. To accomplish this, perform the following steps:
</p>
<ol>
  <li><code>python main.py 4 39 --history --dump-tables</code></li>
  <li><code>python visualization.py --fps 30 --qtable M</code></li>
</ol>

<p>
Consider the case where you wish to simulate experiment 1b with seed 42 and visualize it with agent F's Q-table information. Perhaps you also want to conduct the simulation with the ms reinforcement learning state space. To accomplish this, perform the following steps:
</p>
<ol>
  <li><code>python main.py 1b 42 --history --rl ms --dump-tables</code></li>
  <li><code>python visualization.py --qtable F</code></li>
</ol>

<p><b>Note that you can toggle pause/play using the spacebar when visualizing experiments. While paused, using the right arrow key will advance the agents by a single step. The <code>f</code> and <code>s</code> keys increase and decrease the framerate during simulation. The <code>q</code> key exits the simulation, and the <code>g</code> key captures a screenshot in the current working directory.</b></p>
