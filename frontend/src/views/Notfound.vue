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
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ef 100%);
}

.not-found-content {
  max-width: 500px;
  background-color: white;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 75, 0.1);
  transform: translateY(-20px);
  animation: floatIn 0.5s ease-out forwards;
}

@keyframes floatIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.not-found h1 {
  font-size: 120px;
  margin: 0;
  background: linear-gradient(45deg, #2196F3, #00004b);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  line-height: 1;
  font-weight: 800;
}

.not-found h2 {
  font-size: 30px;
  margin: 0 0 20px;
  color: #333;
  font-weight: 600;
}

.not-found p {
  color: #666;
  margin-bottom: 30px;
  font-size: 16px;
}

.btn-home {
  display: inline-block;
  background: linear-gradient(90deg, #2196F3, #00004b);
  color: white;
  padding: 14px 28px;
  border-radius: 30px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 10px rgba(33, 150, 243, 0.3);
}

.btn-home:hover {
  transform: translateY(-3px);
  box-shadow: 0 7px 15px rgba(33, 150, 243, 0.4);
  background: linear-gradient(90deg, #1976D2, #00003b);
  text-decoration: none;
}
</style>