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
    ![WhatsApp Image 2024-07-10 at 10 26 58 PM](https://github.com/baync180705/Cli-Documentation-Aggregator/assets/146727112/d3a597de-86a5-4324-bc1a-58394ae11af5)

    <p>Once the script starts running, user can type search <scrapper> <term to search> , for examples:</p>
    ![WhatsApp Image 2024-07-10 at 10 27 29 PM](https://github.com/baync180705/Cli-Documentation-Aggregator/assets/146727112/49bdfce1-6c59-42cf-a17e-0e68f83e6cbd)
    ![WhatsApp Image 2024-07-10 at 11 01 40 PM](https://github.com/baync180705/Cli-Documentation-Aggregator/assets/146727112/d5c04a35-9daf-4844-86a7-64158d924657)
    
    <p>User can use : doc show <scrapper> to show previous saved results and select the file based on index</p>
    ![WhatsApp Image 2024-07-10 at 10 29 58 PM](https://github.com/baync180705/Cli-Documentation-Aggregator/assets/146727112/de589050-c161-45b1-980d-da853fcd2122)

    <p>User can use : doc remove <scrapper> to show previous saved results and select the file based on index to delete it</p>
    ![WhatsApp Image 2024-07-10 at 10 29 58 PM](https://github.com/baync180705/Cli-Documentation-Aggregator/assets/146727112/b40e2937-37e9-4771-90a5-3e5fb286ef0d)
    ![WhatsApp Image 2024-07-10 at 10 30 31 PM](https://github.com/baync180705/Cli-Documentation-Aggregator/assets/146727112/f2435c71-686b-4a54-b621-64996447f532)

    <p>User can list down the content of webman directory to show the previous saved outputs</p>
    ![WhatsApp Image 2024-07-10 at 10 28 46 PM](https://github.com/baync180705/Cli-Documentation-Aggregator/assets/146727112/cf6abfc1-4450-4208-bcd8-fd62420660c1)

<br>
<h2>Future Recommendations </h2>
<ul>
    <li>Further testing in order to refine the scrappers </li>
    <li>Building a package out of it to make it scalable</li>
    <li>Add more scrappers</li>
    <li>Prompting user to add his/her API_KEY for using the Google GenAI</li>
</ul>
