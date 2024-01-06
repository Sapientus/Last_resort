# Cut my code into pieces, this is my last resort!
import platform
import asyncio
import aiohttp
import argparse
from datetime import datetime, timedelta


async def main(days):
    info_list = []

    # Asynchration, no syncho. Don't give a f*ck if this function is missing!
    # Ok, I turned this masterpiece off and start to explain. Here I get data  from privatbank, using async with api
    async with aiohttp.ClientSession() as session:
        for i in range(days):
            required_date = (datetime.now() - timedelta(days=i)).strftime("%d.%m.%Y")

            async with session.get(
                f"https://api.privatbank.ua/p24api/exchange_rates?json&date={required_date}"
            ) as response:
                result = await response.json()
                info_list.append(sort_data(result))
        return info_list


# This finds necessary data from what we get, and give us only EUR and USD
def sort_data(data):
    whole_dict = {}
    needed_money = ["EUR", "USD"]
    if data["exchangeRate"]:
        whole_dict[data["date"]] = {}
        for money in needed_money:
            money_dict = {}
            for the_dict in data["exchangeRate"]:
                if the_dict["currency"] == money:
                    money_dict = {
                        "sale": the_dict["saleRateNB"],
                        "purchase": the_dict["purchaseRateNB"],
                    }
                    whole_dict[data["date"]][money] = money_dict
    else:
        whole_dict[data["date"]] = "There is no data about that day"
    return whole_dict


if __name__ == "__main__":
    # This allows to give arguments from terminal
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "days", type=int, help="Number of days to fetch currency rates (up to 10 days)"
    )

    args = parser.parse_args()

    if args.days > 10:
        print("Error: You can fetch currency rates for up to 10 days only.")
    else:
        if (
            platform.system() == "Windows"
        ):  # Checks the system to prevent RunTimeError in Windows
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            r = asyncio.run(main(args.days))
            print(r)
