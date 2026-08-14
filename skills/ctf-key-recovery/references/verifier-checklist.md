# Verifier Checklist

- What exact bytes enter the verifier?
- Is whitespace stripped?
- Is the key length checked before encoding?
- Which encoding converts text to bytes?
- Which constant controls display-only decoding?
- Which constant is compared for success?
- Does the loop use `i % key_length`, a fixed period, or state feedback?
- Are code bytes and constant bytes transformed separately?
- Does success require execution of reconstructed code or only a byte comparison?
- Does the live binary accept the recovered raw key?

