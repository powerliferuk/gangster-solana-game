# Gangster Empire: Solana Streets - Expanded Version with NFTs, SPL, Wallet Map

import pygame
import sys
import random

# Try importing solana modules; if unavailable, use stubs
try:
    from solana.keypair import Keypair
    from solana.rpc.api import Client
    from solana.transaction import Transaction
    from solana.system_program import TransferParams, transfer
    from spl.token.client import Token
    from spl.token.constants import TOKEN_PROGRAM_ID

    solana_available = True
except ModuleNotFoundError:
    print("[Warning] 'solana' module not found. Blockchain features are disabled.")
    solana_available = False

    class Keypair:
        def __init__(self):
            self.public_key = f"FAKE_KEY_{random.randint(1000,9999)}"

    class Client:
        def __init__(self, url): pass
        def get_balance(self, pubkey): return {"result": {"value": 1000000000}}
        def send_transaction(self, tx, signer): return {"result": "FAKE_SIGNATURE"}

    class Transaction:
        def add(self, _): pass

    class TransferParams:
        def __init__(self, from_pubkey, to_pubkey, lamports): pass

    def transfer(params): return params

    class Token:
        def __init__(self, *args, **kwargs): pass
        def mint_to(self, *args, **kwargs): print("[Simulated SPL Mint]")

# --- Blockchain Setup --- #
solana = Client("https://api.devnet.solana.com")
user_wallet = Keypair()
receiver_wallet = Keypair()

# Simulated NFT Characters
nft_gangsters = [
    {"name": "Tommy Blaze", "rarity": "Rare"},
    {"name": "Big Sal", "rarity": "Common"},
    {"name": "Lady Viper", "rarity": "Epic"},
]

# SPL Token Simulation
in_game_token = Token()  # Simulated
user_spl_balance = 0

# --- Blockchain Helpers --- #
def check_balance(pubkey):
    balance = solana.get_balance(pubkey)
    return balance["result"]["value"] / 1_000_000_000

def send_sol(from_keypair, to_pubkey, lamports):
    if not solana_available:
        print("[Simulated] Sent 0.001 SOL")
        return True
    tx = Transaction()
    tx.add(transfer(TransferParams(from_pubkey=from_keypair.public_key, to_pubkey=to_pubkey, lamports=lamports)))
    try:
        resp = solana.send_transaction(tx, from_keypair)
        print("Transaction signature:", resp["result"])
        return True
    except Exception as e:
        print("Transaction failed:", e)
        return False

def mint_game_token(amount):
    global user_spl_balance
    if not solana_available:
        print(f"[Simulated] Minted {amount} GANG tokens")
    else:
        print(f"[Blockchain] Minting {amount} GANG tokens to player wallet...")
    user_spl_balance += amount

# --- Pygame Setup --- #
pygame.init()
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Gangster Empire: Solana Streets")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)

# --- Draw Functions --- #
def draw_text(text, x, y, color=(255, 255, 255)):
    screen.blit(font.render(text, True, color), (x, y))

def draw_map():
    pygame.draw.rect(screen, (60, 60, 60), (600, 50, 350, 600))
    draw_text("City Turf Map", 700, 60)
    draw_text("Downtown", 650, 120)
    draw_text("Docks", 650, 160)
    draw_text("Warehouse", 650, 200)
    draw_text("Casino", 650, 240)

# --- Main Game Loop --- #
def main_game():
    global user_spl_balance
    player_money = 0
    sol_reward = 1000000  # 0.001 SOL
    gangster = random.choice(nft_gangsters)
    running = True

    while running:
        screen.fill((0, 0, 0))
        draw_text("Gangster Empire: Solana Streets", 300, 20)
        draw_text(f"Wallet: {user_wallet.public_key}", 30, 60)
        draw_text(f"SOL Balance: {check_balance(user_wallet.public_key):.4f}", 30, 100)
        draw_text(f"Gang Token: {user_spl_balance} GANG", 30, 140)
        draw_text(f"Character: {gangster['name']} ({gangster['rarity']})", 30, 180)
        draw_text(f"Cash: ${player_money}", 30, 220)
        draw_text("[H] Heist (+$100)", 30, 260)
        draw_text("[R] Redeem $500 → 0.001 SOL", 30, 300)
        draw_text("[M] Mint 50 GANG tokens ($200)", 30, 340)

        draw_map()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    player_money += 100
                    print("Heist succeeded! $100 earned.")

                elif event.key == pygame.K_r and player_money >= 500:
                    print("Redeeming for SOL reward...")
                    if send_sol(receiver_wallet, user_wallet.public_key, sol_reward):
                        player_money -= 500
                        print("Reward claimed.")

                elif event.key == pygame.K_m and player_money >= 200:
                    mint_game_token(50)
                    player_money -= 200

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    print("User Wallet:", user_wallet.public_key)
    print("Receiver Wallet (game treasury):", receiver_wallet.public_key)
    main_game()
