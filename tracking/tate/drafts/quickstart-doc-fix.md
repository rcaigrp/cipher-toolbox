# Quickstart Documentation Improvement

## Issue
The quickstart guide doesn't explicitly state where the checkout directory should be on the target system.

## Current Situation
In the quickstart documentation, there's a step that says:
```
4. Change to your checkout inside the guest:

   .. code-block:: console

      target# cd /workspace/shirudo
```

However, this location isn't explained in the "Before you begin" section or anywhere else in the guide.

## Suggested Improvement
Add a sentence in the "Before you begin" section that explicitly mentions:
- The checkout directory on the target system is expected to be at `/workspace/shirudo`
- This is where the test VM shares the host's checkout

This would make it clearer for users following the quickstart guide.