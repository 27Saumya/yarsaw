from .httpclient import *
from .utils import *
import base64
import aiohttp
from .data_classes import *
from typing import Union


class Client(HTTPClient):
    """
    Represents a client object used to interact with the Random Stuff API.

    Parameters
    ----------
    authorization : :class:`str`
        Your API Key for the Random Stuff API used to authenticate your requests.
    key : :class:`str`
        Your RapidAPI-Key for the Random Stuff API used to authenticate your requests.
    """

    async def get_ai_response(self, message: str, **kwargs) -> AIResponse:
        """
        Gets AI responses from the API.

        Parameters
        -------------
        message: :class:`str`
            The message you want to get the AI response for.
        id: Optional[Union[:class:`str`, :class:`int`]]
            Assign an unique ID for customized response for each user.
        bot_name: Optional[:class:`str`]
            Set a name for the AI replying to your message.
        bot_gender: Optional[:class:`str`]
            Set a gender for the AI replying to your message.
        bot_master: Optional[:class:`str`]
            The creator/master of the AI replying to your message.
        bot_age: Optional[:class:`str`]
            The age of the AI replying to your message.
        bot_company: Optional[:class:`str`]
            The company that owns the AI replying to your message.
        bot_location: Optional[:class:`str`]
            The location of the AI replying to your message.
        bot_email: Optional[:class:`str`]
            The email of the AI replying to your message.
        bot_build: Optional[:class:`str`]
            The build of the AI replying to your message.
        bot_birth_year: Optional[:class:`str`]
            The birth year of the AI replying to your message.
        bot_birth_date: Optional[:class:`str`]
            The birth date of the AI replying to your message.
        bot_birth_place: Optional[:class:`str`]
            The birth place of the AI replying to your message.
        bot_favorite_color: Optional[:class:`str`]
            The favorite color of the AI replying to your message.
        bot_favorite_book: Optional[:class:`str`]
            The favorite book of the AI replying to your message.
        bot_favorite_band: Optional[:class:`str`]
            The favorite band of the AI replying to your message.
        bot_favorite_artist: Optional[:class:`str`]
            The favorite artist of the AI replying to your message.
        bot_favorite_actress: Optional[:class:`str`]
            The favorite actress of the AI replying to your message.
        bot_favorite_actor: Optional[:class:`str`]
            The favorite actor of the AI replying to your message.

        Returns
        -------------
        :class:`AIResponse`
            An object containing the AI response and its details.
        """
        response = await self.request("ai", params={"msg": message, **kwargs})
        return AIResponse(
            response.body["AIResponse"],
            BotDetails(
                response.body["BotDetails"]["BotName"],
                response.body["BotDetails"]["BotMaster"],
                response.body["BotDetails"]["BotAge"],
                response.body["BotDetails"]["BotLocation"],
                response.body["BotDetails"]["BotCompany"],
                response.body["BotDetails"]["BotBirthYear"],
                response.body["BotDetails"]["BotBirthDate"],
                response.body["BotDetails"]["BotBirthPlace"],
            ),
            APIInfo(
                int(response.headers["X-RateLimit-Requests-Limit"]),
                int(response.headers["X-RateLimit-Requests-Remaining"]),
                int(response.headers["X-RateLimit-Requests-Reset"]),
            ),
        )

    async def get_animal_image(self, animal: str, amount: int = 1) -> Image:
        """
        Gets animal images from the API.

        Parameters
        -------------
        animal: :class:`str`
            The animal you want to get images for. Supported Animals: Dog, Cat, Wolf, Fox
        amount: Optional[:class:`int`]
            The amount of images you want to get.

        Returns
        -------------
        :class:`Image`
            An object containing the image.
        """
        try:
            if animal.upper() not in ANIMAL_TYPES:
                raise ValueError(
                    "Animal not supported. Supported animals are: "
                    + ", ".join(ANIMAL_TYPES)
                )
        except AttributeError as e:
            raise ValueError(
                "Invalid Parameter Type. Make sure you are passing a string."
            ) from e

        response = await self.request(
            f"animals/{animal.upper()}", params={"limit": amount}
        )
        images = response.body
        image_list = [image["url"] for image in images]
        return Image(
            image_list,
            APIInfo(
                int(response.headers["X-RateLimit-Requests-Limit"]),
                int(response.headers["X-RateLimit-Requests-Remaining"]),
                int(response.headers["X-RateLimit-Requests-Reset"]),
            ),
        )

    async def get_anime_gif(self, gif_type: str, amount: int = 1) -> Image:
        """
        Gets an anime gif from the API.

        Parameters
        -------------
        gif_type: :class:`str`
            The type of gif you want to get. Allowed Types: happy, hi, kiss, hug, punch, pat, slap, nervous, run, cry
        amount: Optional[:class:`int`]
            The number of gifs you want to get.

        Returns
        -------------
        :class:`Image`
            An object containing the gif.
        """
        try:
            if gif_type.lower() not in ANIME_TYPES:
                raise ValueError(
                    "Invalid Anime GIF Type. Supported types are: "
                    + ", ".join(ANIME_TYPES)
                )
        except AttributeError as e:
            raise ValueError(
                "Invalid Parameter Type. Make sure you are passing a string."
            ) from e

        response = await self.request(
            f"anime/{gif_type.lower()}", params={"limit": amount}
        )
        gifs = response.body
        gif_list = [gif["url"] for gif in gifs]
        return Image(
            gif_list,
            APIInfo(
                int(response.headers["X-RateLimit-Requests-Limit"]),
                int(response.headers["X-RateLimit-Requests-Remaining"]),
                int(response.headers["X-RateLimit-Requests-Reset"]),
            ),
        )

    async def canvas(
        self, method, save_to=None, txt=None, text=None, img1=None, img2=None, img3=None
    ) -> Union[CanvasResponse, int]:

        """
        Edit Images with the API.

        Parameters
        -------------
        method: :class:`str`
            The method to be used to edit the image.

            **Allowed Methods**:

                - Method(s) in which only 1 image is required: ``affect``, ``beautiful``, ``wanted``, ``delete``, ``trigger``, ``facepalm``, ``blur``, ``hitler``, ``kiss``, ``jail``, ``invert``, ``jokeOverHead``
                - Method(s) in which 2 images are required: ``bed``, ``fuse`` , ``kiss``, ``slap``, ``spank``
                - Method(s) in which 3 images are required: ``distracted``
                - Method(s) in which only Text is required: ``changemymind``

        save_to: Optional[:class:`str`]
            The path to save the edited image to. If not specified, the edited image will be returned as bytes.

        txt: Optional[:class:`str`]
            The text required for your method.

        text: Optional[:class:`str`]
            The text required for your method. Alias of txt.

        img1: Optional[:class:`str`]
            The path/link to the first image.

        img2: Optional[:class:`str`]
            The path/link to the second image.

        img3: Optional[:class:`str`]
            The path/link to the third image.

        Returns
        -------------
        Union[:class:`CanvasResponse`, :class:`int`]
            If save_to is not specified, the edited image will be returned as a Response object containing the base64 encoded image.
            If save_to is specified, the edited image will be saved to the specified path, and will 200.

        """
        params = {
            "txt": txt or text or "",
            "img1": img1 or "",
            "img2": img2 or "",
            "img3": img3 or "",
        }

        response = await self.request(f"canvas/{method}", params=params)
        base = response.body["base64"]

        if save_to:
            with open(save_to, "wb") as file:
                file.write(base64.b64decode((base)))
            return 200

        return CanvasResponse(
            base64.b64decode((base)),
            base,
            APIInfo(
                int(response.headers["X-RateLimit-Requests-Limit"]),
                int(response.headers["X-RateLimit-Requests-Remaining"]),
                int(response.headers["X-RateLimit-Requests-Reset"]),
            ),
        )

    async def get_joke(self, joke_type="any", blacklist: list = None) -> Joke:
        """
        Fetches jokes from the API.

        Parameters
        -------------
        joke_type: Optional[:class:`str`]
            The type of joke you want to fetch.
            Allowed Values: "any", "dark", "pun", "spooky", "christmas", "Programming", "misc"

        blacklist: Optional[:class:`list`]
            A list of types jokes you want to blacklist.
            Allowed Values: "all", "nsfw", "religious", "political", "racist", "sexist", "explicit"

        Returns
        -------------
        :class:`Joke`
            An object containing the joke and its details.
        """
        if blacklist is None:
            blacklist = []
        joke_type = joke_type.lower()
        if joke_type.lower() not in JOKE_TYPES:
            supported_types = ", ".join(JOKE_TYPES)
            raise ValueError(f"Invalid Type. Supported types are: {supported_types}")

        # API Bug: The Joke Type Query must be titlecased if the type of joke is "programming"
        if joke_type.lower() == "programming":
            joke_type = "Programming"
        else:
            joke_type = joke_type.lower()

        blist = ""
        if blacklist:
            if "all" in blacklist:
                blist = "nsfw&religious&political&racist&sexist&explicit"
            else:
                blist = "&".join(blacklist)

        response = await self.request(
            f"joke?blacklist={blist}", params={"type": joke_type}
        )

        if response.body["type"] == "twopart":
            return Joke(
                response.body["error"],
                response.body["category"],
                response.body["type"],
                response.body["flags"],
                response.body["id"],
                response.body["safe"],
                response.body["lang"],
                APIInfo(
                    int(response.headers["X-RateLimit-Requests-Limit"]),
                    int(response.headers["X-RateLimit-Requests-Remaining"]),
                    int(response.headers["X-RateLimit-Requests-Reset"]),
                ),
                setup=response.body["setup"],
                delivery=response.body["delivery"],
            )
        return Joke(
            response.body["error"],
            response.body["category"],
            response.body["type"],
            response.body["flags"],
            response.body["id"],
            response.body["safe"],
            response.body["lang"],
            APIInfo(
                int(response.headers["X-RateLimit-Requests-Limit"]),
                int(response.headers["X-RateLimit-Requests-Remaining"]),
                int(response.headers["X-RateLimit-Requests-Reset"]),
            ),
            joke=response.body["joke"],
        )

    async def get_safe_joke(self, joke_type="any") -> Joke:
        """
        Fetches safe jokes from the API. These jokes are family-friendly.

        Parameters
        -------------
        joke_type: Optional[:class:`str`]
            The type of joke you want to fetch.
            Allowed Values: "any", "dark", "pun", "spooky", "christmas", "Programming", "misc"

        Returns
        -------------
        :class:`Joke`
            An object containing the joke and its details.
        """
        joke = await self.get_joke(joke_type=joke_type, blacklist=["all"])
        while joke.safe is not True:
            joke = await self.get_joke(joke_type=joke_type, blacklist=["all"])
        return joke

    async def fetch_subreddit_post(
        self, subreddit: str, search_type: str = "hot"
    ) -> RedditPost:
        """
        Fetches a random post from a subreddit.

        Parameters
        -------------
        subreddit: :class:`str`
            The subreddit to fetch a post from.

        search_type: Optional[:class:`str`]
            This is how it sorts the posts. Allows: "hot", "new", "rising", "top"

        Returns
        -------------
        :class:`RedditPost`
            An object containing the post and its details.
        """
        if search_type.lower() not in SEARCH_TYPES:
            raise ValueError(
                "Invalid Search Type. Supported types are: " + ", ".join(SEARCH_TYPES)
            )

        res = await self.request(
            "reddit/FetchSubredditPost",
            params={"subreddit": subreddit, "searchType": search_type},
        )

        return RedditPost(
            res.body["id"],
            res.body["type"],
            res.body["title"],
            res.body["author"],
            res.body["postLink"],
            res.body["image"],
            res.body["gallery"],
            res.body["text"],
            res.body["thumbnail"],
            res.body["subreddit"],
            res.body["NSFW"],
            res.body["spoiler"],
            res.body["createdUtc"],
            res.body["upvotes"],
            res.body["downvotes"],
            res.body["upvoteRatio"],
            APIInfo(
                int(res.headers["X-RateLimit-Requests-Limit"]),
                int(res.headers["X-RateLimit-Requests-Remaining"]),
                int(res.headers["X-RateLimit-Requests-Reset"]),
            ),
        )

    async def fetch_post(self, subreddit: str, search_type: str = "hot") -> RedditPost:
        """
        Fetches a random post from a subreddit. This is an alias of :meth:`fetch_subreddit_post`.

        Parameters
        -------------
        subreddit: :class:`str`
            The subreddit to fetch a post from.

        search_type: Optional[:class:`str`]
            This is how it sorts the posts. Allows: "hot", "new", "rising", "top"

        Returns
        -------------
        :class:`RedditPost`
            An object containing the post and its details.
        """
        if search_type.lower() not in SEARCH_TYPES:
            raise ValueError(
                "Invalid Search Type. Supported types are: " + ", ".join(SEARCH_TYPES)
            )

        res = await self.request(
            "reddit/FetchPost",
            params={"subreddit": subreddit, "searchType": search_type},
        )

        return RedditPost(
            res.body["id"],
            res.body["type"],
            res.body["title"],
            res.body["author"],
            res.body["postLink"],
            res.body["image"],
            res.body["gallery"],
            res.body["text"],
            res.body["thumbnail"],
            res.body["subreddit"],
            res.body["NSFW"],
            res.body["spoiler"],
            res.body["createdUtc"],
            res.body["upvotes"],
            res.body["downvotes"],
            res.body["upvoteRatio"],
            APIInfo(
                int(res.headers["X-RateLimit-Requests-Limit"]),
                int(res.headers["X-RateLimit-Requests-Remaining"]),
                int(res.headers["X-RateLimit-Requests-Reset"]),
            ),
        )

    async def random_meme(self, search_type: str = "hot") -> RedditPost:
        """
        Gets a random meme from reddit.

        Parameters
        -------------
        search_type: Optional[:class:`str`]
            This is how it sorts the posts. Allows: "hot", "new", "rising", "top"

        Returns
        -------------
        :class:`RedditPost`
            An object containing the post and its details.
        """
        if search_type.lower() not in SEARCH_TYPES:
            raise ValueError(
                "Invalid Search Type. Supported types are: " + ", ".join(SEARCH_TYPES)
            )

        res = await self.request(
            "reddit/RandomMeme", params={"searchType": search_type}
        )
        return RedditPost(
            res.body["id"],
            res.body["type"],
            res.body["title"],
            res.body["author"],
            res.body["postLink"],
            res.body["image"],
            res.body["gallery"],
            res.body["text"],
            res.body["thumbnail"],
            res.body["subreddit"],
            res.body["NSFW"],
            res.body["spoiler"],
            res.body["createdUtc"],
            res.body["upvotes"],
            res.body["downvotes"],
            res.body["upvoteRatio"],
            APIInfo(
                int(res.headers["X-RateLimit-Requests-Limit"]),
                int(res.headers["X-RateLimit-Requests-Remaining"]),
                int(res.headers["X-RateLimit-Requests-Reset"]),
            ),
        )

    async def fetch_random_post(self, search_type: str = "hot") -> RedditPost:
        """
        Fetches a random post from reddit.

        Parameters
        -------------
        search_type: Optional[:class:`str`]
            This is how it sorts the posts. Allows: "hot", "new", "rising", "top"

        Returns
        -------------
        :class:`RedditPost`
            An object containing the post and its details.
        """
        if search_type.lower() not in SEARCH_TYPES:
            raise ValueError(
                "Invalid Search Type. Supported types are: " + ", ".join(SEARCH_TYPES)
            )

        res = await self.request(
            "reddit/FetchRandomPost", params={"searchType": search_type}
        )
        return RedditPost(
            res.body["id"],
            res.body["type"],
            res.body["title"],
            res.body["author"],
            res.body["postLink"],
            res.body["image"],
            res.body["gallery"],
            res.body["text"],
            res.body["thumbnail"],
            res.body["subreddit"],
            res.body["NSFW"],
            res.body["spoiler"],
            res.body["createdUtc"],
            res.body["upvotes"],
            res.body["downvotes"],
            res.body["upvoteRatio"],
            APIInfo(
                int(res.headers["X-RateLimit-Requests-Limit"]),
                int(res.headers["X-RateLimit-Requests-Remaining"]),
                int(res.headers["X-RateLimit-Requests-Reset"]),
            ),
        )

    async def fetch_post_by_id(
        self, post_id: str, search_type: str = "hot"
    ) -> RedditPost:
        """
        Fetch a reddit post by its ID.

        Parameters
        -------------
        post_id: :class:`str`
            The ID of the post to fetch.

        search_type: Optional[:class:`str`]
            This is how it sorts the posts. Allows: "hot", "new", "rising", "top"

        Returns
        -------------
        :class:`RedditPost`
            An object containing the post and its details.
        """
        if search_type.lower() not in SEARCH_TYPES:
            raise ValueError(
                "Invalid Search Type. Supported types are: " + ", ".join(SEARCH_TYPES)
            )

        res = await self.request(
            "reddit/FetchPostById", params={"id": post_id, "searchType": search_type}
        )
        return RedditPost(
            res.body["id"],
            res.body["type"],
            res.body["title"],
            res.body["author"],
            res.body["postLink"],
            res.body["image"],
            res.body["gallery"],
            res.body["text"],
            res.body["thumbnail"],
            res.body["subreddit"],
            res.body["NSFW"],
            res.body["spoiler"],
            res.body["createdUtc"],
            res.body["upvotes"],
            res.body["downvotes"],
            res.body["upvoteRatio"],
            APIInfo(
                int(res.headers["X-RateLimit-Requests-Limit"]),
                int(res.headers["X-RateLimit-Requests-Remaining"]),
                int(res.headers["X-RateLimit-Requests-Reset"]),
            ),
        )

    # NOT TESTED - 401 Unauthorized

    async def get_weather(self, city: str) -> list:
        """
        Gets the weather for a city.

        Parameters
        -------------
        city: :class:`str`
            The city to get the weather for.

        Returns
        -------------
        :class:`list`
            A list containing the weather details.
        """
        res = await self.request("weather", params={"city": city})
        try:
            res.body.append(
                APIInfo(
                    int(res.headers["X-RateLimit-Requests-Limit"]),
                    int(res.headers["X-RateLimit-Requests-Remaining"]),
                    int(res.headers["X-RateLimit-Requests-Reset"]),
                )
            )
        except:
            return res.body
        else:
            return res.body

    ## PREMIUM ENDPOINTS

    async def get_fact(self, fact_type="all") -> Fact:
        """
        Fetches a random fact from the API. PREMIUM ENDPOINT.

        Parameters
        -------------
        fact_type: Optional[:class:`str`]
            The type of fact you want to fetch.

        Returns
        -------------
        :class:`Fact`
            An object containing the fact.
        """
        if fact_type.lower() not in FACT_TYPES:
            raise ValueError(
                "Invalid Fact Type. Supported types are: " + ", ".join(FACT_TYPES)
            )
        res = await self.request(f"facts/{fact_type.lower()}")
        return Fact(
            res.body["fact"],
            APIInfo(
                int(res.headers["X-RateLimit-Requests-Limit"]),
                int(res.headers["X-RateLimit-Requests-Remaining"]),
                int(res.headers["X-RateLimit-Requests-Reset"]),
            ),
        )

    async def get_waifu(self, image_type, waifu_type=None) -> Waifu:
        """
        Fetches SFW or NSFW waifu images from the API. PREMIUM ENDPOINT.

        Parameters
        -------------
        image_type: :class:`str`
            Whether you want SFW or NSFW images.

        waifu_type: Optional[:class:`str`]
            The type of waifu you want to fetch. Visit https://api-docs.pgamerx.com/Documentation/premium/waifu/#available-waifu_types for all available waifu types.

        Returns
        -------------
        :class:`Waifu`
            An object containing the waifu image url.
        """
        if waifu_type is None:
            waifu_type = ""

        res = await self.request(
            f"waifu/{image_type}", params={"waifu_type": waifu_type}
        )
        return Waifu(
            res.body["url"],
            APIInfo(
                int(res.headers["X-RateLimit-Requests-Limit"]),
                int(res.headers["X-RateLimit-Requests-Remaining"]),
                int(res.headers["X-RateLimit-Requests-Reset"]),
            ),
        )

    async def disconnect(self):
        """Closes the Client Session"""
        await self._session.close()

    async def reconnect(self):
        """Restarts the Client Connection"""
        self._session = aiohttp.ClientSession()
