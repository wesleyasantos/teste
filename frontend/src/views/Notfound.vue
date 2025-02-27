<template>
    <div class="not-found">
      <div class="not-found-content">
        <h1>404</h1>
        <h2>Página não encontrada</h2>
        <p>A página que você está procurando não existe ou foi movida.</p>
        <router-link to="/" class="btn-home">Voltar para a página inicial</router-link>
      </div>
    </div>
</template>
  
<script>
export default {
  name: 'NotFound'
}
</script>
  
<style scoped>
.not-found {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 180px);
  text-align: center;
  padding: 20px;
}

.not-found-content {
  max-width: 500px;
}

.not-found h1 {
  font-size: 120px;
  margin: 0;
  color: #2196F3;
  line-height: 1;
}

.not-found h2 {
  font-size: 30px;
  margin: 0 0 20px;
  color: #333;
}

.not-found p {
  color: #666;
  margin-bottom: 30px;
}

.btn-home {
  display: inline-block;
  background-color: #2196F3;
  color: white;
  padding: 12px 24px;
  border-radius: 4px;
  text-decoration: none;
  font-weight: 500;
}

.btn-home:hover {
  background-color: #1976D2;
  text-decoration: none;
}

</style>