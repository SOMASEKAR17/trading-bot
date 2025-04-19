# scheduler.py
import asyncio
import nest_asyncio
from bot import send_signal, update_last_signal, application
from strategy import get_4h_candle, get_current_price
from apscheduler.schedulers.asyncio import AsyncIOScheduler

nest_asyncio.apply()  # Patch event loop to allow nested loops

scheduler = AsyncIOScheduler()
candle_data = {}

@scheduler.scheduled_job("cron", hour=21, minute=0)
async def mark_liquidity_range():
    global candle_data
    candle_data = get_4h_candle()
    if candle_data:
        message = f"🔔 21:00 4H Candle Marked\nHigh: {candle_data['high']}\nLow: {candle_data['low']}"
        await send_signal(message)
        update_last_signal(message)

@scheduler.scheduled_job("interval", minutes=1)
async def monitor_liquidity_grab():
    print("monitor_liquidity_grab is running")
    if not candle_data:
        return
    price = get_current_price()
    high, low = candle_data["high"], candle_data["low"]

    if price > high:
        entry = price
        sl = round(entry + 0.0008, 5)
        tp1 = round(entry - 0.0024, 5)
        tp2 = round(low, 5)
        signal_message = (
            f"📉 Sell Signal – EUR/USD\n"
            f"Entry: {entry}\nSL: {sl}\nTP1: {tp1}\nTP2: {tp2}"
        )
        await send_signal(signal_message)
        update_last_signal(signal_message)
    elif price < low:
        entry = price
        sl = round(entry - 0.0008, 5)
        tp1 = round(entry + 0.0024, 5)
        tp2 = round(high, 5)
        signal_message = (
            f"📈 Buy Signal – EUR/USD\n"
            f"Entry: {entry}\nSL: {sl}\nTP1: {tp1}\nTP2: {tp2}"
        )
        await send_signal(signal_message)
        update_last_signal(signal_message)

async def main():
    scheduler.start()
    
    await application.run_polling()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
