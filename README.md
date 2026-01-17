## Balloons

- [x] Base stats: `HP`, `speed`, `damage`, `reward`
- [x] Movement logic
- [ ] Split logic upon death
- [x] Factory method implementation

## Towers

- [ ] Base stats: `damage`, `range`, `cooldown`, `cost`
- [ ] Define the `attack()` method for override
- [ ] Stat upgrades system
- [ ] Create basic towers with different abilities

## Maps

- [x] Generate map with paths as a tilemap (using AI or algorithm)

## Difficulties

- [ ] **Modifiers:**
  - Shorter path length
  - Faster balloons
  - Higher balloon `HP`
  - Lower spawn delay
  - More balloons per wave
  - Less money earned

## UI

- [ ] **Main Menu:**
  - New Game: difficulty selection
  - Continue: load save file
  - Stats: per game / overall
- [ ] **Save System:**
  - Data: `current round`, `money`, `towers`, `map`
- [ ] **Audio:**
  - Menu: ?
  - Between waves: Calm
  - During waves: KR
