let pathname = window.location.href
    
    const elementoPai = document.getElementById('navbar-nav');
    const filhos = elementoPai.children;

    // Iterar sobre os elementos filhos
    for (let i = 0; i < filhos.length; i++) {
        const filho = filhos[i];

        //pathname.includes(filho.href)
        if(pathname === filho.href){
            filho.classList.add("active")
        } else {
            filho.classList.remove("active")
        }
    }

