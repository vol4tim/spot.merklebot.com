<!-- eslint-disable vue/html-self-closing -->
<template>
  <nav id="navigation" class="p-2 bg-gray-800 font-mono border-b-2 text-white">
    <div class="flex items-center mx-24">
      <NuxtLink to="/" class="flex items-center px-4">
        <img src="/favicon.ico" class="mx-4 h-11" />
        <div class="self-center text-xl">
          MerkleBot
        </div>
      </NuxtLink>
      <ul class="flex flex-row">
        <NuxtLink to="/" class="px-4 mx-4 hover:bg-orange-600">
          Spot
        </NuxtLink>
        <NuxtLink to="/records" class="px-4 mx-4 hover:bg-orange-600">
          Records
        </NuxtLink>
      </ul>
    </div>
  </nav>
</template>
