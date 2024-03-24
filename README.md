# FlickFinder (UC Hacks 24)

Devlopers: Patrick, Drew, Chloe, Theo, Olivia

[Picture of the homepage](./public/demo.png)

## Inspiration

Countless evenings have been lost in the endless scroll, searching for the ideal movie to watch, only to end up watching nothing. This all-too-common dilemma is what motivates us. We aim to transform indecision into action, turning those fruitless searches into moments of discovery and enjoyment.

## What it does

FlickFinder is your go-to movie discovery tool. Just describe what you're in the mood to watch in any words you like, and our platform will present you with a curated list of movies that match your description. To ensure you find the perfect match, FlickFinder offers filters for year, runtime, and rating, tailoring your search results to fit your exact preferences. Say goodbye to endless scrolling and hello to your next favorite movie with FlickFinder :joy:.

## How we built it

**Backend:**
[1] Wrote a function to convert the user's description into JSON format
[2] Used the OpenAI API to generate parameter values (genres, keywords, actors) based on the user's description
[3] Used the TMBD API to narrow down the list of relevant movies based on the parameter values
[4] Created a watchlist using the TMBD API

**Frontend:**
Used Streamlit.io to create our web-app using Python code

##Link
Coming soon!
