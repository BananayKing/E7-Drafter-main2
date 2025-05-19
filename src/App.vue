
<template>
  <div id="app">
    <Navbar>
    </Navbar>
    <router-view />
  

  </div>

 

</template>



<script>
// uvicorn recommender.app.main:app --host 0.0.0.0 --port 8000
import Navbar from "./components/nav.vue";
import CharacterGrid from "./components/CharacterGrid.vue";

export default {
  components: {
    Navbar,
    CharacterGrid
  }
  
};
</script>

