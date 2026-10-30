from dataclasses import dataclass


@dataclass(frozen=True)
class Weapon:
    """Immutable weapon. Instances are shared safely between characters."""

    name: str
    damage: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "damage", int(self.damage))


# Cada arma queda guardada en una variable con su nombre.
daga = Weapon("Daga", 5)
espada_corta = Weapon("Espada corta", 12)
espada_larga = Weapon("Espada larga", 18)
hacha_de_guerra = Weapon("Hacha de guerra", 24)
martillo = Weapon("Martillo", 28)
lanza = Weapon("Lanza", 16)
arco_de_madera = Weapon("Arco de madera", 14)
ballesta = Weapon("Ballesta", 22)
pistola = Weapon("Pistola", 15)
revolver = Weapon("Revolver", 20)
escopeta = Weapon("Escopeta", 35)
subfusil = Weapon("Subfusil", 18)
rifle_de_asalto = Weapon("Rifle de asalto", 30)
rifle_de_francotirador = Weapon("Rifle de francotirador", 55)
lanzallamas = Weapon("Lanzallamas", 40)
granada = Weapon("Granada", 60)
baston_magico = Weapon("Baston magico", 25)
varita_electrica = Weapon("Varita electrica", 32)
rifle_laser = Weapon("Rifle laser", 45)
canon_de_plasma = Weapon("Canon de plasma", 70)

# Lista con todas las armas, por si se necesita recorrer el inventario completo.
weapons = [
    daga,
    espada_corta,
    espada_larga,
    hacha_de_guerra,
    martillo,
    lanza,
    arco_de_madera,
    ballesta,
    pistola,
    revolver,
    escopeta,
    subfusil,
    rifle_de_asalto,
    rifle_de_francotirador,
    lanzallamas,
    granada,
    baston_magico,
    varita_electrica,
    rifle_laser,
    canon_de_plasma,
]

# Explicit exports
__all__ = [
    "Weapon",
    "arco_de_madera",
    "ballesta",
    "baston_magico",
    "canon_de_plasma",
    "daga",
    "escopeta",
    "espada_corta",
    "espada_larga",
    "granada",
    "hacha_de_guerra",
    "lanza",
    "lanzallamas",
    "martillo",
    "pistola",
    "revolver",
    "rifle_de_asalto",
    "rifle_de_francotirador",
    "rifle_laser",
    "subfusil",
    "varita_electrica",
    "weapons",
]
