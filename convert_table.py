#!/usr/bin/env python3
import sys
import os
import re

def parse_time(val):
    val = val.strip().replace('*', '').replace('_', '')
    m = re.match(r'^(\d+)\.(\d+)\.(\d+)$', val)
    if m:
        # e.g., 1.33.40 -> 1:33
        return f"{m.group(1)}:{m.group(2)}"
    m2 = re.match(r'^(\d+)\.(\d+)$', val)
    if m2:
        return f"{m2.group(1)}:{m2.group(2)}"
    return val

def format_value(val, is_variation=False):
    val = val.strip().replace('*', '').replace('_', '')
    if not val:
        return "--"
    
    # If it is a time value formatted as X.YY.ZZ or X.YY
    if re.match(r'^\d+\.\d+\.\d+$', val) or re.match(r'^\d+\.\d+$', val):
        val = parse_time(val)
    
    # Escape percent sign
    if '%' in val:
        val = val.replace('%', '\\%')
        if is_variation:
            # Prepend plus sign for positive values that aren't 0,00% and don't already have a sign
            if val and val[0].isdigit() and not val.startswith('0,00') and not val.startswith('+'):
                val = '+' + val
        return val
        
    # Formatting numbers: 0,200 -> 0,20
    if ',' in val:
        parts = val.split(',')
        if len(parts) == 2 and len(parts[1]) == 3 and parts[1].endswith('0'):
            val = f"{parts[0]},{parts[1][:2]}"
            
    return val

def convert_md_to_latex(md_filepath, table_name, section_name="Generale"):
    if not os.path.exists(md_filepath):
        print(f"Error: File not found {md_filepath}", file=sys.stderr)
        sys.exit(1)
        
    with open(md_filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Split content into sections
    # Sections start with #
    sections = re.split(r'\n(?=# [^#])', content)
    
    target_section_content = None
    for sec in sections:
        lines = sec.strip().split('\n')
        if not lines:
            continue
        sec_title = lines[0].replace('#', '').strip()
        if sec_title.lower() == section_name.lower():
            target_section_content = sec
            break
            
    if not target_section_content:
        # If section not found, fallback to searching the whole file
        target_section_content = content
        
    # Find the table block starting with ## Tabella <table_name>
    tables = re.split(r'\n(?=## Tabella [^#])', target_section_content)
    target_table_content = None
    for tbl in tables:
        lines = tbl.strip().split('\n')
        if not lines:
            continue
        tbl_title = lines[0].replace('##', '').strip()
        # Should match "Tabella C1" or "C1"
        if table_name.lower() in tbl_title.lower():
            target_table_content = tbl
            break
            
    if not target_table_content:
        print(f"Error: Table '{table_name}' not found in section '{section_name}'", file=sys.stderr)
        sys.exit(1)
        
    # Parse the table lines
    lines = target_table_content.strip().split('\n')
    table_lines = [l.strip() for l in lines if l.strip().startswith('|')]
    
    if len(table_lines) < 3:
        print(f"Error: Table content too short or invalid markdown table", file=sys.stderr)
        sys.exit(1)
        
    # Parse rows
    rows_data = []
    current_subgroup = ""
    
    # Row 0: header
    # Row 1: separator (e.g. | :--- | :---: | ...)
    for row in table_lines[2:]:
        # Split by | and filter empty edge items
        cells = [c.strip() for c in row.split('|')]
        # If line starts and ends with |, the split will have empty first and last elements
        if cells and cells[0] == '':
            cells = cells[1:]
        if cells and cells[-1] == '':
            cells = cells[:-1]
            
        if not cells:
            continue
            
        # Check if it is a subgroup header (e.g., | | **Media** | **DEV.ST** | ...)
        first_cell = cells[0].strip().replace('*', '').replace('_', '')
        if first_cell == '':
            # Look for Media or Mediana in subsequent cells
            bold_cells = [c.replace('**', '').strip() for c in cells if '**' in c]
            if bold_cells:
                current_subgroup = bold_cells[0]
            continue
            
        # Data row
        metric_name = first_cell
        # Determine full metric name
        full_metric_name = metric_name
        if current_subgroup and metric_name.lower() not in ['success rate', 'tasso di successo']:
            full_metric_name = f"{current_subgroup} {metric_name}"
            
        # Extract values
        # Col 0: metric
        # Col 1: Versione A
        # Col 2: Versione A (Continuo) / DEV.ST
        # Col 3: Versione B
        # Col 4: Versione B (Continuo) / DEV.ST
        # Col 5: Variazione
        val_a = cells[1] if len(cells) > 1 else ""
        val_b = cells[3] if len(cells) > 3 else ""
        var_val = cells[5] if len(cells) > 5 else ""
        
        formatted_a = format_value(val_a)
        formatted_b = format_value(val_b)
        formatted_var = format_value(var_val, is_variation=True)
        
        rows_data.append((full_metric_name, formatted_a, formatted_b, formatted_var))
        
    # Generate LaTeX
    table_name_lower = table_name.lower()
    
    if section_name.lower() == "generale":
        caption = f"Metriche prestazionali globali aggregate per il compito {table_name}."
        label = f"tab:6-{table_name_lower}-1"
    else:
        caption = f"Confronto delle prestazioni per il compito {table_name} in base all'ordine di esecuzione ({section_name})."
        label = f"tab:6-{table_name_lower}-2"
        
    latex_output = []
    latex_output.append(r"\begin{table}[H]")
    latex_output.append(r"	\centering")
    latex_output.append(r"	\small")
    latex_output.append(r"	\renewcommand{\arraystretch}{1.2}")
    latex_output.append(f"	\\caption{{{caption}}}")
    latex_output.append(f"	\\label{{{label}}}")
    latex_output.append(r"	\begin{tabular}{|>{\raggedright\arraybackslash}p{3cm}|>{\centering\arraybackslash}p{3.8cm}|>{\centering\arraybackslash}p{3.8cm}|>{\centering\arraybackslash}p{2.2cm}|}")
    latex_output.append(r"		\hline")
    latex_output.append(r"		\rowcolor{gray!30}")
    latex_output.append(r"		\textbf{Metrica} & \textbf{Versione originale (A)} & \textbf{Versione post-riprogettazione (B)} & \textbf{Variazione} \\ \hline")
    
    for metric, a, b, var in rows_data:
        # Align LaTeX format
        metric_padded = f"{metric:<16}"
        a_padded = f"{a:<32}"
        b_padded = f"{b:<44}"
        var_padded = f"{var:<21}"
        latex_output.append(f"		{metric_padded} & {a_padded} & {b_padded} & {var_padded} \\\\ \\hline")
        
    latex_output.append(r"	\end{tabular}")
    latex_output.append(r"\end{table}")
    
    return "\n".join(latex_output)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python convert_table.py <table_name> <section_name> [output_file]")
        sys.exit(1)
        
    tbl_name = sys.argv[1]
    sec_name = sys.argv[2]
    out_file = sys.argv[3] if len(sys.argv) > 3 else None
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    md_file = os.path.join(script_dir, "tabelle_analisi.md")
    
    latex = convert_md_to_latex(md_file, tbl_name, sec_name)
    
    if out_file:
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(latex)
        print(f"LaTeX table saved to {out_file}")
    else:
        print(latex)
