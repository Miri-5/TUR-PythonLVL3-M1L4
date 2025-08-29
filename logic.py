import aiohttp  # Eşzamansız HTTP istekleri için bir kütüphane
import random

class Pokemon:
    pokemons = {}
    # Nesne başlatma (kurucu)
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.hp = random.randint(200,400)
        self.power = random.randint(30,60)
        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer]

    async def get_name(self):
        # PokeAPI aracılığıyla bir pokémonun adını almak için asenktron metot
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API
        async with aiohttp.ClientSession() as session:  #  HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve çözümlenmesi
                    return data['forms'][0]['name']  #  Pokémon adını döndürme
                else:
                    return "Pikachu"  # İstek başarısız olursa varsayılan adı döndürür

    async def info(self):
        # Pokémon hakkında bilgi döndüren bir metot
        if not self.name:
            self.name = await self.get_name()  # Henüz yüklenmemişse bir adın geri alınması
        return f""" Pokemon ismi: {self.name}
                    Pokemon gücü: {self.power}
                    Pokemon sağlığı: {self.hp}"""  # Pokémon adını içeren dizeyi döndürür

    async def show_img(self):
        # PokeAPI aracılığıyla bir pokémon görüntüsünün URL'sini almak için asenktron metot
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    img_url= data["sprites"]["front_default"]
                    return img_url
                else:
                    return None 
    
    async def attack(self, enemy):
        if isinstance(enemy, Wizard):  # Düşmanın Wizard veri tipi olup olmadığının kontrol edilmesi (Sihirbaz sınıfının bir örneği midir?) 
                chance = random.randint(1, 5) 
                if chance == 1:
                    return "Sihirbaz Pokémon, kendi canını artırdı"
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ne saldırdı\n@{enemy.pokemon_trainer}'nin sağlık durumu {enemy.hp}"
        else:
            enemy.hp = 0
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ni yendi!"
        
class Fighter(Pokemon):
    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)
        # Dövüşçülere daha fazla güç
        self.power += 20  

    async def info(self):
        base_info = await super().info()
        return "Dövüşçü pokémonunuz var.\n" + base_info

    async def attack(self, enemy):
        super_power = random.randint(5,15)
        self.power += super_power
        result = await super().attack(enemy) 
        self.power -= super_power
        # Eğer kazandıysa bonus ekle
        if enemy.hp == 0:
            self.power += 10
            result += f"\nDövüşçü Pokémon zafer kazandı! Bonus +10 güç eklendi."
        return result + f"\nDövüşçü Pokémon süper saldırı kullandı. Eklenen güç: {super_power}"


class Wizard(Pokemon):
    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)
        # Sihirbazlara daha fazla sağlık
        self.hp += 100  

    async def info(self):
        base_info = await super().info()
        return "Sihirbaz pokémonunuz var.\n" + base_info

    async def attack(self, enemy):
        result = await super().attack(enemy)
        # Eğer kazandıysa bonus ekle
        if enemy.hp == 0:
            self.hp += 50
            result += f"\nSihirbaz Pokémon zafer kazandı! Bonus +50 sağlık eklendi."
        return result

    async def heal(self):
        heal_amount = random.randint(20,50)
        self.hp += heal_amount
        return f"Sihirbaz Pokémon kendini iyileştirdi! +{heal_amount} sağlık. Yeni sağlık: {self.hp}"


if __name__ == '__main__':
    import asyncio
    wizard = Wizard("username1")
    fighter = Fighter("username2")

    print(asyncio.run(wizard.info()))
    print(asyncio.run(fighter.info()))
    print(asyncio.run(fighter.attack(wizard)))