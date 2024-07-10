<h1>CLI DOCUMENTATION AGGREGATOR</h1>
<h2>Introduction</h2>
<p>Our team has developed a documentation aggregator for popular languages and frameworks which runs python scripts in the backend and scraps data from the respective webpages and displays the output on terminal similar to the working of manpages and further saves and retrieves the ouput displayed in text files and csv files (for scrapped tables)</p>
<br>
<h2>Features</h2>
<ul>
    <li>Scrapes documentations React Docs,Flutter Docs,Expressjs docs, Python docs, Django docs and learning platform like Geeks for Geeks</li>
    <li>Displays results on CLI as text similar to the working of manpages</li>
    <li>Falls back to Google Generative AI-generated responses if no result is found and also allows user to even generate responses from Google Generative AI directly</li>
    <li>Allows storage and retrieval of results for further use in the form of text and csv files</li>
    <li>CLI-based, accessible from the terminal in CodeEditor, easing the search process while coding, by just running the main.py script</li>
</ul>
<br>
<h2>Setting up</h2>
<ul>
    <li>Ensure you have python3 installed in your system as some of the dependencies may depend upon it</li>
    <li>Run <strong>pip install -r requirements.txt</strong> (ensure your terminal indicates that you are in the root folder before running this command)</li>
    <li>in case of google gen ai requirement, you may need to run <strong>pip install -U google-generativeai</strong> (in case of module not found error)</li>
    <li>Requires env file for api key for Google GenAI</li>
</ul>
<br>
<h2>Working</h2>

 <p>After setting up the files, open the terminal and run main.py cli to run interactive cli and see the help page</p>
    <img src="./assets/WhatsApp Image 2024-07-10 at 10.26.58 PM.jpeg">

<p>Once the script starts running, user can type search <scrapper> <term_to_search> , for examples:</p>
   <img src="./assets/WhatsApp Image 2024-07-10 at 10.27.29 PM.jpeg"> 
   <img src="./assets/WhatsApp Image 2024-07-10 at 11.01.40 PM.jpeg"> 

    
<p>User can use : doc show <scrapper> to show previous saved results and select the file based on index</p>
    <img src="./assets/WhatsApp Image 2024-07-10 at 11.01.40 PM.jpeg">

<p>User can use : doc remove <scrapper> to show previous saved results and select the file based on index to delete it</p>
   <img src="./assets/WhatsApp Image 2024-07-10 at 10.30.31 PM.jpeg">

<p>User can list down the content of webman directory to show the previous saved outputs</p>
   <img src ="./assets/WhatsApp Image 2024-07-10 at 10.28.46 PM.jpeg"> 

<br>
<h2>Future Recommendations </h2>
<ul>
    <li>Further testing in order to refine the scrappers </li>
    <li>Building a package out of it to make it scalable</li>
    <li>Add more scrappers</li>
    <li>Prompting user to add his/her API_KEY for using the Google GenAI</li>
</ul>
