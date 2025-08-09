# flake8: noqa


import asyncio
import os
from dotenv import load_dotenv
from typing import Any
from mcp.server.fastmcp import FastMCP
from stockfish import Stockfish, StockfishException
import logging

load_dotenv()
userdata = os.environ
STOCKFISH_PATH = userdata.get("STOCKFISH_PATH")
mcp = FastMCP("stockfish")


@mcp.tool()
async def get_best_moves(fen: str, user_elo_rating: int | str = 3300) -> list | str:
    """
    Asynchronously calculates the best moves for a given chess position using the Stockfish engine.

    Args:
        fen (str): The FEN (Forsyth-Edwards Notation) string representing the current chessboard state.
        user_elo_rating (int | str): The ELO rating of the user, which can be used to adjust the engine's playing strength, default being 3000 elo.

    Returns:
        list: A list of the best moves suggested by the Stockfish engine for the given position.
    """
    stockfish = Stockfish(path=STOCKFISH_PATH, parameters={"UCI_Elo": user_elo_rating})

    try:
        if not stockfish.is_fen_valid(fen):
            return "The input fen String is invalid"

        stockfish.set_fen_position(fen)
        res = stockfish.get_top_moves(3)

        return res
    except StockfishException as se:
        return f"Exception while finding top moves:{se}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
