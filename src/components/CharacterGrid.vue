<template>

  <div class="draft-container "    tabindex="0">
    <!-- Draft Left Side (Flipped) -->

    <div class="draft-side left-draft">
      <div class = "team-label">
        <h4>My Team</h4>
      </div>
          <label class="first-pick-label">
      <input type="checkbox" v-model="firstPickSide" true-value="left" false-value=""   />
      First Pick 
    </label>
      <div v-for="n in 5" :tabindex="0"            @keydown.enter.prevent="selectDraftCharacter(n, 'left')" key="'left-' + n" class="draft-placeholder" @click="selectDraftCharacter(n, 'left')">
        <div v-if="draftLeft[n]" class="drafted-character">
          <img 
            :src="'src/data/face/' + draftLeft[n].code + '_l.png'" 
            :alt="draftLeft[n].name" 
            class="draft-image flipped-image"
          />
          <div class="character-info flipped-text">
            <p class="character-name">{{ draftLeft[n].name }}</p>
          </div>
          <div class="character-details">
            <img v-for="i in draftLeft[n]?.rarity" 
                   :key="'star-' + i" 
                   src="../data/img/cm_icon_star.png" 
                   alt="Star" 
                   class="star" />
            <img v-if="draftLeft[n]?.attribute" 
                 :src="'src/data/img/cm_icon_pro' + draftLeft[n].attribute.toLowerCase() + '.png'" 
                 :alt="draftLeft[n].attribute" 
                 class="icon" />
                 <div class="stars">

            </div>
          </div>
          
        </div>
      </div>
      <button @click="clearDraft('left')" v-if="Object.keys(draftLeft).length" class="clear-button">Clear All</button>
    </div>
        <!-- New Recommended Draft Box -->
    <div class="recommended-draft">
      <h4>Recommended Draft</h4>
      <button @click="getDraftState">Calculate Draft</button>

      <div v-if="recommendations.length">
  <div 
    v-for="rec in recommendations" 
    :key="rec.heroid" 
    class="recommendation-card"
    style="display: flex; align-items: center; margin-bottom: 10px; gap: 10px;"
  >
    <img :src="'src/data/face/' + rec.heroid + '_s.png'"  alt="Hero" style="width: 60px; height: 60px;" />
    <div>
      <strong>{{ rec.hero_name }}</strong><br />
      Score: {{ rec.score.toLocaleString() }}<br />
      Slot: {{ rec.slot_score }} | Synergy: {{ rec.syn_score }} | Counter: {{ rec.cnt_score }}
    </div>
  </div>
</div>
<div v-else>
  <em>No recommendations yet. Click Calculate Draft.</em>
</div>
    </div>
    <!-- Character Grid (Center) -->
    <div class="character-grid-container">
      <div class="character-container">
        <div class="controls" style="display: flex; flex-wrap: wrap; gap: 10px; align-items: center;">
  <!-- Rarity Icons -->
<div class="rarity-filter" style="display: flex; gap: 5px;">
  <div
    v-for="star in [3, 4, 5]"
    :key="star"
    :class="{ active: selectedRarity == star.toString() }"
    :style="{
      cursor: 'pointer',
      display: 'flex',
      alignItems: 'center',
      gap: '2px',
      padding: '4px 6px',
      borderRadius: '4px',
      backgroundColor:'#444c5e',

      border: selectedRarity == star.toString() ? '1px solid #77aaff' : '1px solid transparent'
    }"
    @click="selectedRarity = selectedRarity == star.toString() ? '' : star.toString()"
  >
    <img
      v-for="i in star"
      :key="i"
      src="../data/img/cm_icon_star.png"
      style="width: 16px; height: 16px; filter: brightness(1.2);"
    />
  </div>
</div>


  <!-- Attribute Icons -->
  <div class="attribute-filter" style="display: flex; gap: 8px;">
    <img
      v-for="attr in ['Fire', 'Ice', 'Wind', 'Light', 'Dark']"
      :key="attr"
      :src="'src/data/img/cm_icon_pro' + attr.toLowerCase() + '.png'" 
      :class="{ active: selectedAttribute === attr }"
      style="width: 32px; height: 32px; cursor: pointer;"
      @click="selectedAttribute = selectedAttribute === attr ? '' : attr"
    />
  </div>
<div class="role-filter" style="display: flex; gap: 8px; margin-top: 8px;">
  <div
    v-for="role in ['warrior', 'knight', 'assassin', 'ranger', 'mage', 'manauser']"
    :key="role"
    :title="role.charAt(0).toUpperCase() + role.slice(1)"
    :style="{
      padding: '4px',
      borderRadius: '4px',
      backgroundColor: selectedRole === role ? '#444c5e' : '#2e2e2e',
      border: selectedRole === role ? '1px solid #77aaff' : '1px solid transparent',
      cursor: 'pointer'
    }"
    @click="selectedRole = selectedRole === role ? '' : role"
  >
    <img
      :src="'src/data/img/cm_icon_role_' + role + '.png'"
      :alt="role"
      style="width: 24px; height: 24px; filter: brightness(1.2);"
    />
  </div>
</div>
  <!-- Search Bar -->
  <input
  type="text"
  v-model="searchQuery"
  placeholder="Search by name..."
  style="width: 60%; box-sizing: border-box; padding: 6px; margin-top: 8px;"
/>
    <button @click="clearFilters" style="padding: 6px 12px;">Clear Filters</button>
    <button @click="ToggleOwned" style="padding: 6px 12px;">Toggle Owned</button>

</div>

        <div class="character-grid">
          <div
            v-for="character in filteredCharacters"
            :key="character.code"
            class="character-card"
            tabindex="0"
            role="button"
            @click="selectCharacter(character)"
            @keydown.enter.prevent="selectCharacter(character)"
            :class="{ selected: selectedCharacterId === character.code }"
          >
            <img :src="'src/data/face/' + character.code + '_s.png'" :alt="character.name" />
            <h3>{{ character.name }}</h3>
          </div>
        </div>
      </div>
    </div>

    <!-- Draft Right Side (Normal) -->
    <div class="draft-side right-draft "    tabindex="0">
      
               <div class = "team-label">
        <h4>Enemy Team</h4>
          </div>
      <label class="first-pick-label">

      <input type="checkbox" v-model="firstPickSide" true-value="right" false-value=""/>
      First Pick
    </label>
      <div v-for="n in 5" :tabindex="0"             @keydown.enter.prevent="selectDraftCharacter(n, 'right')"key="'right-' + n" class="draft-placeholder" @click="selectDraftCharacter(n, 'right')">
        <div v-if="draftRight[n]" class="drafted-character">
          <img 
            :src="'src/data/face/' + draftRight[n].code + '_l.png'" 
            :alt="draftRight[n].name" 
            class="draft-image"
          />
          <div class="character-info">
            <p class="character-name">{{ draftRight[n].name }}</p>
          </div>
          <div class="character-details">
            <img v-if="draftRight[n]?.attribute" 
                 :src="'src/data/img/cm_icon_pro' + draftRight[n].attribute.toLowerCase() + '.png'" 
                 :alt="draftRight[n].attribute" 
                 class="icon" />
            <div class="stars">
              <img v-for="i in draftRight[n]?.rarity" 
                   :key="'star-' + i" 
                   src="../data/img/cm_icon_star.png" 
                   alt="Star" 
                   class="star" />
            </div>
          
          </div>
        </div>
      </div>
      <button @click="clearDraft('right')" v-if="Object.keys(draftRight).length" class="clear-button">Clear All</button>
    </div>
  </div>
</template>


<script>
import characterData from "../data/herodata.json";
import { API_BASE_URL } from './config';
export default {
  data() {
    return {
      characters: Object.values(characterData),
      allCharacters: Object.values(characterData), // keep full backup
      selectedRarity: "",
      selectedAttribute: "",
      searchQuery: "",
      selectedCharacterId: null,
      draftLeft: {},
      draftRight: {},
      firstPickSide: "left", // "left" or "right",
      recommendations: [],
      selectedRole: "",
    };
  },

  computed: {
filteredCharacters() {
  return this.characters.filter(character => {
    return (
      (!this.selectedRarity || character.rarity == this.selectedRarity) &&
      (!this.selectedAttribute || character.attribute.toLowerCase() === this.selectedAttribute.toLowerCase()) &&
      (!this.selectedRole || character.role.toLowerCase() === this.selectedRole.toLowerCase()) &&
      (!this.searchQuery || character.name.toLowerCase().includes(this.searchQuery.toLowerCase()))
    );
  });
}
  },

  methods: {
     clearFilters() {
    this.selectedRarity = "";
    this.selectedAttribute = "";
    this.selectedRole = "";
    this.searchQuery = "";
  },
  async ToggleOwned() {
  if (this.showOnlyOwned) {
    // revert to full list
    this.characters = this.allCharacters;
    this.showOnlyOwned = false;
    this.clearFilters();
    return;
  }
},
async getDraftState() {
  const firstPick = this.firstPickSide;
  const pickMap = firstPick === "left"
    ? {
        left: { 1: 1, 2: 4, 3: 5, 4: 8, 5: 9 },
        right: { 1: 2, 2: 3, 3: 6, 4: 7, 5: 10 }
      }
    : {
        right: { 1: 1, 2: 4, 3: 5, 4: 8, 5: 9 },
        left: { 1: 2, 2: 3, 3: 6, 4: 7, 5: 10 }
      };

  const draft = [];
  const buildEntry = (side, slot, char) => ({
    pick_order: pickMap[side][slot],
    Team: side === "left" ? "My Team" : "Enemy Team",
    Hero: char.code,
    first_pick: side === firstPick ? 1 : 0
  });

  for (const [slotStr, char] of Object.entries(this.draftLeft)) {
    const slot = parseInt(slotStr);
    if (char) draft.push(buildEntry("left", slot, char));
  }

  for (const [slotStr, char] of Object.entries(this.draftRight)) {
    const slot = parseInt(slotStr);
    if (char) draft.push(buildEntry("right", slot, char));
  }

  const sortedDraft = draft.sort((a, b) => a.pick_order - b.pick_order);

  let selectable_characters = [];

  try {
    const res = await fetch(API_BASE_URL + "/user/characters", {
      credentials: "include"
    });

    if (res.ok) {
      const data = await res.json();
      if (Array.isArray(data.characters)) {
        selectable_characters = data.characters;
      } else {
        console.warn("Invalid characters response:", data);
      }
    } else {
      console.warn("Failed to load /user/characters:", res.status);
    }
  } catch (err) {
    console.warn("Error fetching /user/characters:", err);
  }

  try {
    const payload = {
      picks: sortedDraft,
      ...(selectable_characters.length > 0 && { selected_characters: selectable_characters })
    };

    console.log("Sending payload to /recommend:", payload);

    const recRes = await fetch(API_BASE_URL + '/recommend', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    if (!recRes.ok) throw new Error(`HTTP ${recRes.status}`);

    const recData = await recRes.json();
    this.recommendations = recData.recommendations;

  } catch (err) {
    console.error("API call to /recommend failed:", err);
    alert("API call failed: " + err.message);
  }
},


  selectCharacter(character) {
      this.selectedCharacterId =
        this.selectedCharacterId === character.code ? null : character.code;
    },


    selectDraftCharacter(slot, side) {
      if (!this.selectedCharacterId) return;

      const selected = this.characters.find(
        c => c.code === this.selectedCharacterId
      );

      if (side === "left" && !this.draftLeft[slot]) {
        this.draftLeft[slot] = selected;
        this.selectedCharacterId = null;
      } else if (side === "right" && !this.draftRight[slot]) {
        this.draftRight[slot] = selected;
        this.selectedCharacterId = null;
      }
    },

    clearDraft(side) {
      if (side === "left") {
        this.draftLeft = {};
      } else if (side === "right") {
        this.draftRight = {};
      }
    }
  }
};
</script>

<style scoped>

/* Wrapper for the entire character grid and sticky controls */
.character-grid-wrapper {
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  height: 70vh; /* Control the height of the grid */
  width: 100%;
}

/* Controls area - sticky on top of the character grid */
.controls {
  position: sticky;
  top: 0;
  z-index: 10;
  background-color: #181818;
  padding: 15px 20px;
  margin-bottom: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2); /* Optional shadow for emphasis */
}

/* Styling for select and input elements within controls */
.controls select,
.controls input {
  margin: 5px;
  padding: 8px;
  font-size: 16px;
  background-color: #282828;
  border: 1px solid #444;
  border-radius: 4px;
  color: #fff;
  width: 150px;
}

/* Character grid container */
.character-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); /* Responsive grid */
  gap: 10px;
  justify-items: center;
  padding: 0 10px; /* Ensure characters aren't touching the edges */
  overflow-y: auto; /* Allow scrolling */
  max-height: 65vh; /* Limit height for scrolling effect */
}

/* Individual character card */
.character-card {
  background-color: #282828;
  padding: 15px;
  border-radius: 8px;
  cursor: pointer;
  text-align: center;
  transition: 0.3s;
  border: 2px solid transparent;
  margin-bottom: 10px; /* Space between cards */
  width: 100%; /* Ensures card fills available space */
  max-width: 180px; /* Max width for larger screens */
}

/* Selected character card styling */
.character-card.selected {
  border-color: #ffcc00; /* Yellow border for selected character */
}

/* Hover effect for character cards */
.character-card:hover {
  transform: scale(1.05); /* Slight scaling for hover effect */
}

/* Character image inside the card */
.character-card img {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 5px;
  margin-bottom: 10px; /* Space between image and text */
}

/* Character name and details */
.character-card h3 {
  margin: 5px 0;
  font-size: 16px;
}

.character-card h3,p {
  font-size: 14px;
  color: #bbb; /* Light gray text */
}

/* Hover effect for draft slots */
.draft-placeholder:hover {
  transform: scale(1.05);
}


.drafted-character img {
  height: 100%;
  
}



/* Character info overlay */


.character-name{
  padding-top:10px;
}



/* Draft Slot Titles */
.draft-placeholder p {
  font-size: 18px;
  font-weight: bold;
  color: #bbb;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
  
}



.clear-button:hover {
  background-color: darkred;
}
.icon {
  width:30px !important;  /* Set icon width */
  height: 30px !important ; /* Set icon height */
}



.first-pick-label input[type="checkbox"] {
  margin-right: 5px;
  transform: scale(1.2);
}
.icon {
  width: 30px;
  height: 30px;
}
.image-flip {
  transform: scaleX(1) !important;
}
.team-label{
  position:relative;
  color:#bbb;
  font-weight: bold;
}
/* === DRAFT CONTAINER === */
.draft-container {
  display: flex;
  justify-content: space-between;
  margin: 20px;
  gap: 40px;
}

/* === EACH DRAFT SIDE === */
.draft-side {
  width: 20%;
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-width: 350px;
}

/* === DRAFT BOX === */
.draft-placeholder {
  position: relative;
  width: 100%;
  height: 12vh;
  background-color: #1e1e1e;
  border-radius: 6px;
  overflow: hidden;
  padding: 8px;
  box-sizing: border-box;
  cursor: pointer;
  display: flex;
  justify-content: flex-start;
  align-items: flex-end;
}

/* === CHARACTER IMAGE === */
.draft-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
  z-index: 1;
  border-radius: 6px;
  opacity: 0.95;
}

/* Mirror image on left side */
.left-draft .draft-image {
  transform: scaleX(-1);
  object-position: right;

}
.right-draft .draft-image {
  object-position: right;
}
/* === CHARACTER INFO (OPPOSITE SIDE ALIGNMENT) === */
.character-info {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  color: white;
  text-shadow: 0 0 4px black;
  font-size: 14px;
  width: 100%;
}
.flipped-text{
  position: absolute;
  right:10px;
  bottom:45px;

}
/* On left draft: align text right */
.left-draft .character-info {
  align-items: flex-end;
  text-align: left;


}

/* On right draft: align text left */
.right-draft .character-info {
  align-items: flex-start;
  text-align: left;
}

/* === CHARACTER DETAILS === */
.character-details {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 4px;
  z-index: 2;
  position: absolute;
}
.left-draft .character-details{
  z-index: 2;
  position: absolute;
  right:10px;
  bottom:5px;
}
.right-draft .character-details{
  z-index: 2;
  position: absolute;
  left:10px;
  bottom:5px;
}
/* ICON (attribute) */
.icon {
  width: 20px;
  height: 20px;
  object-fit: cover;
}

/* STARS */
.stars {
  display: flex;
  gap: 2px;
}

.star {
  width: 16px;
  height: 16px;
  object-fit: cover;
}

/* === FIRST PICK LABEL === */
.first-pick-label {
  margin-bottom: 10px;
  font-size: 14px;
  color: #ccc;
  display: flex;
  align-items: center;
  gap: 6px;
}

/* === CLEAR BUTTON === */
.clear-button {
  margin-top: 10px;
  padding: 6px 10px;
  font-size: 14px;
  background-color: #333;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.recommended-draft {
  width: 30%;
  background-color: #1e1e1e;
  border-radius: 6px;
  padding: 15px;
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #bbb;
  font-weight: bold;
  max-width: 400px;
}

.recommended-draft button {
  margin-top: 20px;
  padding: 10px 15px;
  font-size: 16px;
  background-color: #333;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.recommended-draft button:hover {
  background-color: darkgreen;
}
.active {
  filter: brightness(1.2);
  border: 1px solid #aaa;
  border-radius: 4px;
}

</style>
