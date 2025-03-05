import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from django.conf import settings
import os
import joblib

class CreditRiskPredictor:
    def __init__(self):
        self.model_path = os.path.join(settings.BASE_DIR, 'ai_models', 'models', 'credit_risk_model.joblib')
        self.scaler_path = os.path.join(settings.BASE_DIR, 'ai_models', 'models', 'scaler.joblib')
        
        # Carregar modelo treinado se existir, ou criar um novo
        try:
            self.model = joblib.load(self.model_path)
            self.scaler = joblib.load(self.scaler_path)
        except FileNotFoundError:
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            self.scaler = StandardScaler()
    
    def _preprocess_data(self, client, application):
        """
        Prepara os dados do cliente e da aplicação para o modelo de ML.
        """
        # Criar features
        features = {
            'idade': (pd.Timestamp.now().date() - client.birth_date).days / 365.25,
            'renda_mensal': float(client.monthly_income),
            'valor_solicitado': float(application.amount_requested),
            'prazo_meses': application.term_months,
            'valor_parcela': float(application.amount_requested) / application.term_months,
            'percentual_renda': (float(application.amount_requested) / application.term_months) / float(client.monthly_income) * 100
        }
        
        # Adicionar score se disponível
        try:
            credit_score = client.credit_score
            features['score'] = credit_score.score
            features['historico_pagamento'] = credit_score.payment_history
            features['carga_divida'] = credit_score.debt_burden
        except:
            # Valores padrão se não houver score
            features['score'] = 500
            features['historico_pagamento'] = 50
            features['carga_divida'] = 50
        
        # Converter para dataframe
        df = pd.DataFrame([features])
        
        # Escalar dados
        scaled_features = self.scaler.transform(df)
        
        return scaled_features
    
    def predict(self, client, application):
        """
        Faz a predição de risco para um cliente e aplicação.
        """
        X = self._preprocess_data(client, application)
        
        # Predição de probabilidade
        default_probability = self.model.predict_proba(X)[0, 1]
        
        # Risk score (0-100, menor é melhor)
        risk_score = default_probability * 100
        
        # Gerar recomendação
        recommendation = self._generate_recommendation(risk_score, client, application)
        
        # Gerar explicação
        explanation = self._generate_explanation(risk_score, client, application)
        
        return {
            'risk_score': risk_score,
            'default_probability': default_probability,
            'recommendation': recommendation,
            'explanation': explanation
        }
    
    def _generate_recommendation(self, risk_score, client, application):
        """
        Gera uma recomendação baseada no score de risco.
        """
        monthly_payment = float(application.amount_requested) / application.term_months
        income_ratio = monthly_payment / float(client.monthly_income)
        
        if risk_score < 20:
            return "APROVADO: Risco baixo, excelente candidato para aprovação."
        elif risk_score < 40:
            return "APROVADO COM CONDIÇÕES: Bom candidato, mas considerar redução do valor ou aumento do prazo."
        elif risk_score < 60:
            return "ANÁLISE MANUAL: Risco moderado, recomendada revisão manual do histórico e documentos."
        elif risk_score < 80:
            return "REPROVADO COM CONDIÇÕES: Alto risco, considerar apenas com garantias adicionais ou fiador."
        else:
            return "REPROVADO: Risco muito alto, não recomendada aprovação."
    
    def _generate_explanation(self, risk_score, client, application):
        """
        Gera uma explicação detalhada da análise.
        """
        monthly_payment = float(application.amount_requested) / application.term_months
        income_ratio = monthly_payment / float(client.monthly_income) * 100
        
        explanation = f"Score de risco: {risk_score:.2f}/100 (quanto menor, melhor)\n\n"
        
        # Análise da capacidade de pagamento
        explanation += "Análise de capacidade de pagamento:\n"
        explanation += f"- Valor da parcela: R$ {monthly_payment:.2f}\n"
        explanation += f"- Comprometimento da renda: {income_ratio:.2f}% da renda mensal\n"
        
        # Fatores de decisão
        explanation += "\nPrincipais fatores para a decisão:\n"
        
        if income_ratio > 30:
            explanation += "- NEGATIVO: Alto comprometimento da renda (acima de 30%)\n"
        else:
            explanation += "- POSITIVO: Bom comprometimento da renda (abaixo de 30%)\n"
        
        try:
            if client.credit_score.score < 500:
                explanation += "- NEGATIVO: Score de crédito baixo\n"
            else:
                explanation += "- POSITIVO: Score de crédito adequado\n"
        except:
            explanation += "- NEUTRO: Sem informações de score de crédito\n"
        
        # Recomendações adicionais
        if risk_score > 40:
            explanation += "\nSugestões para melhorar a análise:\n"
            explanation += "- Solicitar comprovantes adicionais de renda\n"
            explanation += "- Verificar histórico detalhado de pagamentos\n"
            explanation += "- Considerar redução do valor solicitado ou aumento do prazo\n"
        
        return explanation
    
    def train(self, X, y):
        """
        Treina o modelo com novos dados.
        """
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
        
        # Salvar modelo treinado
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.scaler, self.scaler_path)

# Interface para o Django
def run_ai_model(application):
    """
    Função para ser chamada pela API do Django para gerar uma nova predição.
    """
    from ai_models.models import AIPrediction
    
    predictor = CreditRiskPredictor()
    client = application.client
    
    prediction_result = predictor.predict(client, application)
    
    # Salvar a predição no banco
    prediction = AIPrediction.objects.create(
        client=client,
        application=application,
        risk_score=prediction_result['risk_score'],
        default_probability=prediction_result['default_probability'],
        recommendation=prediction_result['recommendation'],
        explanation=prediction_result['explanation']
    )
    
    return prediction