import httpx
from fastmcp import FastMCP

mcp = FastMCP("Currency MCP Server")


@mcp.tool()
async def get_latest_rates(base: str = "EUR", symbols: str | None = None) -> dict:
    """Retrieve the latest exchange rates.

    Args:
        base: The base currency symbol (default: EUR).
        symbols: A comma-separated list of target currency symbols to filter.
    """
    async with httpx.AsyncClient() as client:
        params = {}
        if base:
            params["base"] = base
        if symbols:
            params["symbols"] = symbols
        response = await client.get(
            "https://api.frankfurter.dev/v1/latest", params=params
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_historical_rates(
    date: str, base: str | None = None, symbols: str | None = None
) -> dict:
    """Retrieve exchange rates for a specific past date.

    Args:
        date: The date in YYYY-MM-DD format.
        base: The base currency symbol.
        symbols: A comma-separated list of target currency symbols.
    """
    async with httpx.AsyncClient() as client:
        params = {}
        if base:
            params["base"] = base
        if symbols:
            params["symbols"] = symbols
        response = await client.get(
            f"https://api.frankfurter.dev/v1/{date}", params=params
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_time_series_rates(
    start_date: str,
    end_date: str | None = None,
    base: str | None = None,
    symbols: str | None = None,
) -> dict:
    """Retrieve exchange rates over a specific time period.

    Args:
        start_date: Start date (YYYY-MM-DD).
        end_date: End date (YYYY-MM-DD). If omitted, defaults to the current date.
        base: The base currency symbol.
        symbols: A comma-separated list of target currency symbols.
    """
    url = f"https://api.frankfurter.dev/v1/{start_date}.."
    if end_date:
        url += end_date

    async with httpx.AsyncClient() as client:
        params = {}
        if base:
            params["base"] = base
        if symbols:
            params["symbols"] = symbols
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_available_currencies() -> dict:
    """Retrieve a list of all available currency symbols and their full names."""
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.frankfurter.dev/v1/currencies")
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    mcp.run(transport="http", port=8080)
