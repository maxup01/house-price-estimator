from enum import Enum

class SpainCity(Enum):
    """
    Spanish cities/locations for thinkSPAIN property searches.
    The value is the URL slug used in /es/venta-viviendas/{slug}.
    """

    # Major cities
    MADRID = "madrid"
    BARCELONA = "barcelona"
    VALENCIA = "valencia"
    MALAGA = "malaga"
    ALICANTE = "alicante"
    MURCIA = "murcia"
    GRANADA = "granada"
    ALMERIA = "almeria"
    CADIZ = "cadiz"
    SEVILLA = "sevilla"
    CORDOBA = "cordoba"
    GIRONA = "girona"
    TARRAGONA = "tarragona"
    CASTELLON = "castellon"

    # Costa del Sol / Andalucía (near you)
    MARBELLA = "marbella"
    ESTEPONA = "estepona"
    MIJAS = "mijas"
    BENAHAVIS = "benahavis"
    MAZARRON = "mazarron"
    ORIHUELA = "orihuela"

    # Costa Blanca
    TORREVIEJA = "torrevieja"
    DENIA = "denia"
    CALPE = "calpe"

    # Islands
    MALLORCA = "mallorca"
    PALMA_DE_MALLORCA = "palma-de-mallorca"
    TENERIFE = "tenerife"
    IBIZA = "ibiza"
    GRAN_CANARIA = "gran-canaria"
    FUERTEVENTURA = "fuerteventura"
    LANZAROTE = "lanzarote"
    MENORCA = "menorca"

    # Regions / coasts (also valid search slugs)
    COSTA_BLANCA = "costa-blanca"
    COSTA_DEL_SOL = "costa-del-sol"
    COSTA_CALIDA = "costa-calida"
    COSTA_BRAVA = "costa-brava"
