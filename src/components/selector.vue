<template>
  <div class="character-grid-wrapper">
    <!-- Left grid -->
    <div class="character-grid-container">
      <h2>Selected Characters</h2>
        <button @click="confirmChanges" class="btn-confirm">Confirm Changes</button>
      
      <!-- Filters for Left -->
      <div class="controls" style="display: flex; flex-wrap: wrap; gap: 10px; align-items: center;">
        <!-- Rarity -->
        <div class="rarity-filter" style="display: flex; gap: 5px;">
          <div
            v-for="star in [3,4,5]"
            :key="star"
            :class="{ active: selectedRarityLeft == star.toString() }"
            @click="selectedRarityLeft = selectedRarityLeft == star.toString() ? '' : star.toString()"
            style="cursor:pointer; padding:4px 6px; border-radius:4px; background:#444c5e; display:flex; gap:2px; align-items:center;"
          >
            <img
              v-for="i in star"
              :key="i"
              src="../data/img/cm_icon_star.png"
              style="width: 16px; height: 16px; filter: brightness(1.2);"
            />
          </div>
        </div>
        
        <!-- Attribute -->
        <div class="attribute-filter" style="display: flex; gap: 8px;">
          <img
            v-for="attr in ['Fire', 'Ice', 'Wind', 'Light', 'Dark']"
            :key="attr"
            :src="'src/data/img/cm_icon_pro' + attr.toLowerCase() + '.png'"
            :class="{ active: selectedAttributeLeft === attr }"
            @click="selectedAttributeLeft = selectedAttributeLeft === attr ? '' : attr"
            style="width: 32px; height: 32px; cursor: pointer;"
          />
        </div>
        
        <!-- Role -->
        <div class="role-filter" style="display: flex; gap: 8px; margin-top: 8px;">
          <div
            v-for="role in ['warrior', 'knight', 'assassin', 'ranger', 'mage', 'manauser']"
            :key="role"
            :title="role.charAt(0).toUpperCase() + role.slice(1)"
            @click="selectedRoleLeft = selectedRoleLeft === role ? '' : role"
            :style="{
              padding: '4px',
              borderRadius: '4px',
              backgroundColor: selectedRoleLeft === role ? '#444c5e' : '#2e2e2e',
              border: selectedRoleLeft === role ? '1px solid #77aaff' : '1px solid transparent',
              cursor: 'pointer'
            }"
          >
            <img
              :src="'src/data/img/cm_icon_role_' + role + '.png'"
              :alt="role"
              style="width: 24px; height: 24px; filter: brightness(1.2);"
            />
          </div>
        </div>
        
        <!-- Search -->
        <input
          type="text"
          v-model="searchQueryLeft"
          placeholder="Search by name..."
          style="width: 60%; box-sizing: border-box; padding: 6px; margin-top: 8px;"
        />
        
        <button @click="clearFiltersLeft" style="padding: 6px 12px;">Clear Filters</button>
        <button @click="addAll" style="padding: 6px 12px;">Add All</button>
<button @click="removeAll" style="padding: 6px 12px;">Remove All</button>
      </div>

      <!-- Left Characters Grid -->
      <div class="character-grid" v-if="filteredLeftCharacters.length">
        <div
          v-for="character in filteredLeftCharacters"
          :key="character.code"
          class="character-card"
          @click="removeFromLeft(character)"
          :class="{ selected: selectedCharacterIdLeft === character.code }"
        >
          <img :src="'src/data/face/' + character.code + '_s.png'" :alt="character.name" />
          <h3>{{ character.name }}</h3>
        </div>
      </div>
      <p v-else style="color: #aaa; margin-top: 20px;">No characters selected yet.</p>
    </div>

    <!-- Right grid -->
    <div class="character-grid-container">
      <h2>All Characters</h2>
      
      <!-- Filters for Right -->
      <div class="controls" style="display: flex; flex-wrap: wrap; gap: 10px; align-items: center;">
        <!-- Rarity -->
        <div class="rarity-filter" style="display: flex; gap: 5px;">
          <div
            v-for="star in [3,4,5]"
            :key="star"
            :class="{ active: selectedRarityRight == star.toString() }"
            @click="selectedRarityRight = selectedRarityRight == star.toString() ? '' : star.toString()"
            style="cursor:pointer; padding:4px 6px; border-radius:4px; background:#444c5e; display:flex; gap:2px; align-items:center;"
          >
            <img
              v-for="i in star"
              :key="i"
              src="../data/img/cm_icon_star.png"
              style="width: 16px; height: 16px; filter: brightness(1.2);"
            />
          </div>
        </div>
        
        <!-- Attribute -->
        <div class="attribute-filter" style="display: flex; gap: 8px;">
          <img
            v-for="attr in ['Fire', 'Ice', 'Wind', 'Light', 'Dark']"
            :key="attr"
            :src="'src/data/img/cm_icon_pro' + attr.toLowerCase() + '.png'"
            :class="{ active: selectedAttributeRight === attr }"
            @click="selectedAttributeRight = selectedAttributeRight === attr ? '' : attr"
            style="width: 32px; height: 32px; cursor: pointer;"
          />
        </div>
        
        <!-- Role -->
        <div class="role-filter" style="display: flex; gap: 8px; margin-top: 8px;">
          <div
            v-for="role in ['warrior', 'knight', 'assassin', 'ranger', 'mage', 'manauser']"
            :key="role"
            :title="role.charAt(0).toUpperCase() + role.slice(1)"
            @click="selectedRoleRight = selectedRoleRight === role ? '' : role"
            :style="{
              padding: '4px',
              borderRadius: '4px',
              backgroundColor: selectedRoleRight === role ? '#444c5e' : '#2e2e2e',
              border: selectedRoleRight === role ? '1px solid #77aaff' : '1px solid transparent',
              cursor: 'pointer'
            }"
          >
            <img
              :src="'src/data/img/cm_icon_role_' + role + '.png'"
              :alt="role"
              style="width: 24px; height: 24px; filter: brightness(1.2);"
            />
          </div>
        </div>
        
        <!-- Search -->
        <input
          type="text"
          v-model="searchQueryRight"
          placeholder="Search by name..."
          style="width: 60%; box-sizing: border-box; padding: 6px; margin-top: 8px;"
        />
        
        <button @click="clearFiltersRight" style="padding: 6px 12px;">Clear Filters</button>
      </div>

      <!-- Right Characters Grid -->
      <div class="character-grid">
        <div
          v-for="character in filteredRightCharacters"
          :key="character.code"
          class="character-card"
          @click="addToLeft(character)"
          :class="{ selected: selectedCharacterIdRight === character.code }"
        >
          <img :src="'src/data/face/' + character.code + '_s.png'" :alt="character.name" />
          <h3>{{ character.name }}</h3>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import characterData from "../data/herodata.json";
import { API_BASE_URL } from './config';

export default {
  data() {
    return {
      allCharacters: Object.values(characterData),  // full list for right grid
      leftCharacters: [],  // starts empty
      rightCharacters: Object.values(characterData),  // all chars initially visible on right
      isLoggedIn: false,
      username: '',

      // Filters for left grid
      selectedRarityLeft: "",
      selectedAttributeLeft: "",
      selectedRoleLeft: "",
      searchQueryLeft: "",

      // Filters for right grid
      selectedRarityRight: "",
      selectedAttributeRight: "",
      selectedRoleRight: "",
      searchQueryRight: "",

      selectedCharacterIdLeft: null,
      selectedCharacterIdRight: null,
    };
  },

  computed: {
    filteredLeftCharacters() {
      return this.leftCharacters.filter(character => {
        return (
          (!this.selectedRarityLeft || character.rarity == this.selectedRarityLeft) &&
          (!this.selectedAttributeLeft || character.attribute.toLowerCase() === this.selectedAttributeLeft.toLowerCase()) &&
          (!this.selectedRoleLeft || character.role.toLowerCase() === this.selectedRoleLeft.toLowerCase()) &&
          (!this.searchQueryLeft || character.name.toLowerCase().includes(this.searchQueryLeft.toLowerCase()))
        );
      });
    },

    filteredRightCharacters() {
      return this.rightCharacters.filter(character => {
        return (
          (!this.selectedRarityRight || character.rarity == this.selectedRarityRight) &&
          (!this.selectedAttributeRight || character.attribute.toLowerCase() === this.selectedAttributeRight.toLowerCase()) &&
          (!this.selectedRoleRight || character.role.toLowerCase() === this.selectedRoleRight.toLowerCase()) &&
          (!this.searchQueryRight || character.name.toLowerCase().includes(this.searchQueryRight.toLowerCase()))
        );
      });
    },
  },
mounted() {
  this.checkAuth();
},
  methods: {
    
    async confirmChanges() {
    try {
      const response = await fetch(API_BASE_URL + '/user/characters/save', {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(this.leftCharacters.map(c => c.code)), // assuming left grid is selected
      });
      if (response.ok) {
        alert('Saved successfully');
      } else {
        alert('Login to save');
      }
    } catch (e) {
      alert('Error: ' + e.message);
    }
  },
    addAll() {
    // Add all filteredRightCharacters to leftCharacters, avoid duplicates
    const newChars = this.filteredRightCharacters.filter(rChar => 
      !this.leftCharacters.some(lChar => lChar.code === rChar.code)
    );
    this.leftCharacters.push(...newChars);
  },
  removeAll() {
    this.leftCharacters = [];
  },
     removeFromLeft(character) {
    this.leftCharacters = this.leftCharacters.filter(c => c.code !== character.code);
  },
    clearFiltersLeft() {
      this.selectedRarityLeft = "";
      this.selectedAttributeLeft = "";
      this.selectedRoleLeft = "";
      this.searchQueryLeft = "";
    },
    clearFiltersRight() {
      this.selectedRarityRight = "";
      this.selectedAttributeRight = "";
      this.selectedRoleRight = "";
      this.searchQueryRight = "";
    },
    addToLeft(character) {
      if (!this.leftCharacters.find(c => c.code === character.code)) {
        this.leftCharacters.push(character);
      }
      
    },
    selectCharacterLeft(character) {
      this.selectedCharacterIdLeft = character.code;
    },
    selectCharacterRight(character) {
      this.selectedCharacterIdRight = character.code;
    },

  async checkAuth() {
  try {
    const res = await fetch(API_BASE_URL + "/auth/me", {
      credentials: "include"
    });

    if (!res.ok) {
      console.warn("Not authenticated.");
      return;
    }

    const user = await res.json();
    this.isLoggedIn = true;
    this.username = user.email;
    console.log("Logged in as:", this.username);
    await this.loadSavedCharacters();
  } catch (err) {
    console.error("Failed to check auth", err);
  }
},

async loadSavedCharacters() {
  try {
    const res = await fetch(API_BASE_URL + "/user/characters", {
      credentials: "include"
    });
    if (!res.ok) return;

    const data = await res.json();
    const heroCodes = data.characters;
    if (!Array.isArray(heroCodes)) {
      console.error("Invalid characters response", data);
      return;
    }

    this.leftCharacters = this.allCharacters.filter(char =>
      heroCodes.includes(char.code)
    );
  } catch (err) {
    console.error("Failed to load characters", err);
  }
},

  mounted() {
  this.loadSavedCharacters();
}
  }
};
</script>

<style scoped>
h2 {
  color: #bbb;               /* subtle bright blue */
  font-weight: 600;             /* semi-bold */
  font-size: 1.75rem;           /* slightly smaller */
  padding: 10px 16px;           /* less padding */
  border-radius: 4px;           /* gentle rounding */
  letter-spacing: 1px;          /* slight spacing */
  user-select: none;
}
.left-grid, .right-grid {
  flex: 1;
  display: flex;
  flex-direction: column;
}
.grid-wrapper {
  display: flex;
  gap: 20px;
  width: 100%;
}
/* Wrapper for the entire character grid and sticky controls */
.character-grid-wrapper {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  gap: 20px;
}
.character-grid-container {
  flex: 1;
  max-width: 50%;
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
.btn-confirm {
  margin-left: 10px;
  padding: 4px 8px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.btn-confirm:hover {
  background-color: #0056b3;
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
}
.left-draft .character-details{
  z-index: 4;
  position: absolute;
  right:10px;
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
