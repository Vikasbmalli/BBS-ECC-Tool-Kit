"""Blum Blum Shub (BBS) pseudorandom bit generator - educational implementation."""

import argparse
import math


def is_probable_prime(n: int) -> bool:
    """Simple deterministic trial-division check, suitable only for small demo inputs."""
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def validate_parameters(p: int, q: int, seed: int) -> int:
    if p == q:
        raise ValueError("p and q must be different primes.")
    if not is_probable_prime(p) or not is_probable_prime(q):
        raise ValueError("p and q must both be prime (demo checker supports small values).")
    if p % 4 != 3 or q % 4 != 3:
        raise ValueError("Both p and q must be congruent to 3 modulo 4.")
    n = p * q
    if not 1 < seed < n:
        raise ValueError("Seed must be between 2 and n-1.")
    if math.gcd(seed, n) != 1:
        raise ValueError("Seed must be relatively prime to n.")
    return n


def generate_bits(p: int, q: int, seed: int, count: int):
    if count < 1:
        raise ValueError("Bit count must be at least 1.")
    n = validate_parameters(p, q, seed)
    x = pow(seed, 2, n)
    bits = []
    states = []
    for _ in range(count):
        x = pow(x, 2, n)
        states.append(x)
        bits.append(str(x & 1))
    return "".join(bits), states, n


def main():
    parser = argparse.ArgumentParser(description="Generate pseudorandom bits using Blum Blum Shub.")
    parser.add_argument("--p", type=int, default=383, help="prime p, p mod 4 = 3")
    parser.add_argument("--q", type=int, default=503, help="prime q, q mod 4 = 3")
    parser.add_argument("--seed", type=int, default=101, help="seed relatively prime to p*q")
    parser.add_argument("--count", type=int, default=32, help="number of bits to generate")
    args = parser.parse_args()

    try:
        bits, states, n = generate_bits(args.p, args.q, args.seed, args.count)
    except ValueError as exc:
        parser.error(str(exc))

    print("\n=== Blum Blum Shub (BBS) Generator ===")
    print(f"p = {args.p}, q = {args.q}")
    print(f"n = p*q = {n}")
    print(f"Seed = {args.seed}")
    print(f"Generated {args.count} bits:")
    print(bits)
    print("\nFirst 10 internal states (for classroom demonstration only):")
    for i, state in enumerate(states[:10], start=1):
        print(f"x{i} = {state}")


if __name__ == "__main__":
    main()
