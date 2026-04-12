<template>
  <router-view />
</template>


<style>
:root {
  --primary-orange: #FF8A00;
  --secondary-blue: #4A90E2;
  --bg-light: #F9FAFC;
}

html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

#app {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  overflow-y: auto;
}

#app::-webkit-scrollbar {
  width: 6px;
}

#app::-webkit-scrollbar-track {
  background: transparent;
}

#app::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 10px;
}

#app::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.2);
}

</style>