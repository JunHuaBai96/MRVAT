import numpy as np


def tcmintegration(template_file, template0_file, template1_file, output_file):
    out = []

    # Read the content of template0 file and add it to the output
    with open(template0_file, "r", encoding="utf-8") as f0:
        out.extend(f0.readlines())

    # Add a newline to separate the template0 content and the dynamic content
    out.append('\n')

    # Read the template file lines
    with open(template_file, "r", encoding="utf-8") as f:
        template_lines = f.readlines()

    # Generate State_set for Si and Fe
    State_set = []
    for Si in np.arange(0, 1 + 0.01, 0.01).astype(np.float32):
        for Fe in np.arange(0, 1 + 0.01, 0.01).astype(np.float32):
            if Si + Fe <= 1 and not (Si == 0 and Fe == 0) and not (Si == 1 and Fe == 0):
                State_set.append([Fe, Si])

    # Process each state and replace placeholders
    for state in State_set:
        data_base = {
            'Fe': f"{state[0]:.2f}",
            'Si': f"{state[1]:.2f}"
        }
        write = []

        for line in template_lines:
            new_line = line
            if '%' in line:
                for key in data_base:
                    new_line = new_line.replace(f'%{key}%', data_base[key])
            write.append(new_line)

        # Append additional lines after each group
        write.append('\n')  # Empty line as required
        out.extend(write)

    # Add a newline before appending the content of template1 file
    out.append('\n')

    # Read the content of template1 file and add it to the output
    with open(template1_file, "r", encoding="utf-8") as f1:
        out.extend(f1.readlines())

    # Write the final output to the output file
    with open(output_file, 'w', encoding="utf-8") as fp:
        fp.write(''.join(out))


# Specify the template, template0, template1, and output file paths
template_file = 'template.txt'
template0_file = 'template0.txt'
template1_file = 'template1.txt'
output_file = 'Alltcm.tcm'
tcmintegration(template_file, template0_file, template1_file, output_file)
