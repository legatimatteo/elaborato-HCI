# Configurazione di VS Code per LaTeX su Windows

Questa guida descrive come configurare **Visual Studio Code** su **Windows** per compilare documenti LaTeX in modo efficiente e automatizzato.

---

## 1. Prerequisiti

Per poter compilare file LaTeX all'interno di VS Code, è necessario installare tre componenti fondamentali:

1. **Una distribuzione LaTeX** (es. TeX Live o MiKTeX) per fornire i compilatori (pdflatex, xelatex, lualatex, ecc.).
2. **Un interprete Perl** (es. Strawberry Perl), necessario per il funzionamento di `latexmk` (il tool di automazione usato di default).
3. **Visual Studio Code** con l'estensione **LaTeX Workshop**.

---

## 2. Metodi di Installazione

### A. Installazione di una Distribuzione LaTeX
Si consiglia l'uso di **TeX Live** per la sua completezza e stabilità, ma **MiKTeX** è un'ottima alternativa più leggera.

#### Opzione 1: TeX Live (Consigliato)
1. Scarica l'installer web di TeX Live dal sito ufficiale: [Installing TeX Live over the net](https://www.tug.org/texlive/acquire-netinstall.html).
2. Avvia l'installer (`install-tl-windows.exe`).
3. Seleziona **"Install"** e attendi il completamento (l'installazione completa può richiedere del tempo e diversi GB di spazio).
4. *Nota: Assicurati che l'opzione per aggiungere TeX Live al `PATH` di sistema sia spuntata durante l'installazione.*

#### Opzione 2: MiKTeX (Alternativa leggera)
1. Scarica l'installer da [miktex.org](https://miktex.org/download).
2. Esegui l'installer e segui le istruzioni a schermo.
3. MiKTeX ha una funzionalità comoda che installa automaticamente i pacchetti mancanti "on-the-fly" durante la prima compilazione.

---

### B. Installazione di Perl (Richiesto per `latexmk`)
`latexmk` è uno script scritto in Perl che automatizza la compilazione (esegue pdflatex, bibtex e pdflatex di nuovo se necessario).

1. Scarica **Strawberry Perl** da [strawberryperl.com](https://strawberryperl.com/).
2. Esegui l'installer `.msi` scaricato.
3. L'installer configurerà automaticamente il `PATH` di sistema.

---

### C. Installazione e Configurazione di VS Code

1. Scarica e installa **VS Code** da [code.visualstudio.com](https://code.visualstudio.com/).
2. Apri VS Code e vai nella sezione Estensioni (`Ctrl+Shift+X`).
3. Cerca e installa l'estensione **LaTeX Workshop** (sviluppata da *James Yu*).

---

## 3. Configurazione e Utilizzo

Una volta installati tutti i prerequisiti, **riavvia il computer** (o riavvia VS Code e il terminale) per assicurarti che tutte le variabili d'ambiente (`PATH`) siano caricate correttamente.

### Compilazione di un file
1. Apri una cartella contenente un file `.tex` (ad esempio, aprendo questo workspace in VS Code).
2. Apri il file `.tex` principale (es. [main.tex](file:///home/matteo/Developer/github/elaborato-HCI/main.tex)).
3. Premi **`Ctrl+Alt+B`** per avviare la compilazione automatica.
4. Per visualizzare il PDF generato:
   - Clicca sull'icona della scheda "LaTeX" nella barra laterale sinistra.
   - Clicca su **"View LaTeX PDF"** -> **"View in VS Code tab"** (oppure usa la scorciatoia **`Ctrl+Alt+V`**).

### Compilazione al salvataggio (Auto-build)
Di default, LaTeX Workshop compila il documento ogni volta che salvi il file `.tex`. Se desideri disabilitare o personalizzare questo comportamento, puoi aggiungere la seguente configurazione nel file `settings.json` di VS Code:

```json
{
  "latex-workshop.latex.autoBuild.run": "onSave" // Valori possibili: "onSave", "onFileChange", "never"
}
```

---

## 4. Risoluzione dei Problemi

* **Errore: `latexmk: command not found` o simile**
  * Assicurati che Perl sia installato correttamente digitando `perl -v` in un prompt dei comandi (CMD o PowerShell).
  * Assicurati che la tua distribuzione LaTeX sia nel PATH digitando `pdflatex --version`.
  * Se ricevi errori, prova a riavviare Windows per applicare le modifiche alle variabili d'ambiente.
* **File di ausilio nella cartella**
  * La compilazione genera molti file temporanei (`.aux`, `.log`, `.out`, ecc.). LaTeX Workshop li pulisce automaticamente se configurato, oppure puoi premere `Ctrl+Alt+C` per pulirli manualmente.
