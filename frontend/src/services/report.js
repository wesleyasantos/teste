import { jsPDF } from 'jspdf';
import 'jspdf-autotable';

export default {
  generateOperationReport(operation, client, analysis, committee) {
    const doc = new jsPDF();
    
    // Título
    doc.setFontSize(16);
    doc.text(`Dossiê da Operação #${operation.id}`, 14, 20);
    
    // Informações da operação
    doc.setFontSize(12);
    doc.text('Informações da Operação', 14, 30);
    
    const operationData = [
      ['Cliente', client.name],
      ['CPF/CNPJ', client.document],
      ['Valor', `R$ ${parseFloat(operation.amount).toLocaleString('pt-BR')}`],
      ['Prazo', `${operation.term_months} meses`],
      ['Taxa de Juros', `${operation.interest_rate}% ${operation.interest_frequency}`],
      ['Status', operation.status],
      ['Data de Criação', new Date(operation.created_at).toLocaleDateString('pt-BR')]
    ];
    
    doc.autoTable({
      startY: 35,
      head: [['Campo', 'Valor']],
      body: operationData,
      theme: 'striped',
      headStyles: { fillColor: [0, 0, 75] }
    });
    
    // Análise de crédito
    if (analysis) {
      doc.text('Análise de Crédito', 14, doc.autoTable.previous.finalY + 10);
      
      const analysisData = [
        ['Setor', analysis.sector],
        ['ROB', `R$ ${parseFloat(analysis.pgdas_total).toLocaleString('pt-BR')}`],
        ['Despesa Setorial', `R$ ${parseFloat(analysis.sector_expense).toLocaleString('pt-BR')}`],
        ['Lucro Bruto', `R$ ${parseFloat(analysis.gross_profit).toLocaleString('pt-BR')}`],
        ['Disponibilidade Mensal 1', `R$ ${parseFloat(analysis.availability1).toLocaleString('pt-BR')}`],
        ['Disponibilidade Mensal 2', `R$ ${parseFloat(analysis.availability2).toLocaleString('pt-BR')}`],
        ['Parcela Mensal', `R$ ${parseFloat(operation.installments[0]?.amount || 0).toLocaleString('pt-BR')}`],
        ['Superávit/Déficit', `R$ ${parseFloat(analysis.surplus).toLocaleString('pt-BR')}`],
        ['Decisão', analysis.approved ? 'APROVADO' : 'REPROVADO']
      ];
      
      doc.autoTable({
        startY: doc.autoTable.previous.finalY + 15,
        head: [['Item', 'Valor']],
        body: analysisData,
        theme: 'striped',
        headStyles: { fillColor: [0, 0, 75] }
      });
    }
    
    // Comitê
    if (committee && committee.members.length > 0) {
      doc.text('Comitê de Crédito', 14, doc.autoTable.previous.finalY + 10);
      
      const committeeData = committee.members.map(member => [
        member.name,
        member.role,
        member.vote === 'approve' ? 'Aprovado' : member.vote === 'reject' ? 'Reprovado' : 'Pendente',
        member.voted_at ? new Date(member.voted_at).toLocaleDateString('pt-BR') : '-',
        member.notes || '-'
      ]);
      
      doc.autoTable({
        startY: doc.autoTable.previous.finalY + 15,
        head: [['Membro', 'Cargo', 'Voto', 'Data', 'Observações']],
        body: committeeData,
        theme: 'striped',
        headStyles: { fillColor: [0, 0, 75] }
      });
    }
    
    // Data de emissão
    doc.setFontSize(10);
    doc.text(`Relatório gerado em ${new Date().toLocaleDateString('pt-BR')} às ${new Date().toLocaleTimeString('pt-BR')}`, 14, doc.internal.pageSize.height - 10);
    
    // Salvar PDF
    doc.save(`operacao_${operation.id}.pdf`);
  }
};