document.addEventListener('DOMContentLoaded', function() {

    function aplicarMascara(elementId, funcaoMascara) {
        const elemento = document.getElementById(elementId);
        if (elemento) {
            elemento.addEventListener('input', function(e) {
                // Lógica de cursor comentada por enquanto para focar na formatação
                // const originalValue = e.target.value;
                // const originalPos = e.target.selectionStart;
                const valorFormatado = funcaoMascara(e.target.value);
                e.target.value = valorFormatado;
            });
        }
    }

    // Máscara para RG (formato XX.XXX.XXX-Y)
    function mascaraRG(valor) {
        let v = valor.replace(/[^0-9xX]/gi, '').toUpperCase(); 
        if (v.length > 9) v = v.slice(0, 9); 

        let resultado = "";
        for (let i = 0; i < v.length; i++) {
            resultado += v[i];
            if (i === 1 && v.length > 2) resultado += "."; 
            else if (i === 4 && v.length > 5) resultado += "."; 
            else if (i === 7 && v.length > 8) resultado += "-"; 
        }
        return resultado;
    }
    aplicarMascara('id_rg', mascaraRG);

    // Máscara para CPF (XXX.XXX.XXX-XX)
    function mascaraCPF(valor) {
        let v = valor.replace(/\D/g, ''); 
        if (v.length > 11) v = v.slice(0, 11);

        let resultado = "";
        for (let i = 0; i < v.length; i++) {
            resultado += v[i];
            if (i === 2 && v.length > 3) resultado += ".";
            else if (i === 5 && v.length > 6) resultado += ".";
            else if (i === 8 && v.length > 9) resultado += "-";
        }
        return resultado;
    }
    aplicarMascara('id_cpf', mascaraCPF);

    // Máscara para CEP (XXXXX-XXX)
    function mascaraCEP(valor) {
        let v = valor.replace(/\D/g, ''); // Remove tudo que não é dígito
        if (v.length > 8) v = v.slice(0, 8); // Limita a 8 dígitos

        let resultado = "";
        for (let i = 0; i < v.length; i++) {
            resultado += v[i];
            if (i === 4 && v.length > 5) resultado += "-";
        }
        return resultado;
    }
    aplicarMascara('id_cep', mascaraCEP);

    // Máscara para Telefone ((XX) XXXXX-XXXX ou (XX) XXXX-XXXX)
    function mascaraTelefone(valor) {
        let v = valor.replace(/\D/g, '');
        let len = v.length;

        if (len > 11) v = v.slice(0, 11);
        len = v.length;

        let resultado = "";
        if (len === 0) return ""; // Retorna vazio se não houver dígitos

        resultado = "(";
        for (let i = 0; i < len; i++) {
            resultado += v[i];
            if (i === 1 && len > 2) resultado += ") "; 
            else if (len === 11 && i === 6 && i < len -1) resultado += "-"; // Celular com 9º dígito
            else if (len === 10 && i === 5 && i < len -1) resultado += "-"; // Fixo ou celular antigo
        }
        return resultado;
    }
    
    aplicarMascara('id_telefone', mascaraTelefone); 
    aplicarMascara('id_telefone_principal', mascaraTelefone); 
    aplicarMascara('id_telefone_secundario', mascaraTelefone);
});
