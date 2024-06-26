#!/bin/bash
#
# Script de exemplo para submeter trabalho que não use MPI 
#
#SBATCH --job-name=nomeDoTrabalho          # Nome do trabalho a ser executado (para melhor identificação)
#SBATCH --partition=open_cpu             # Em qual fila o trabalho será executado (ver filas disponíveis com o comando sinfo)
#SBATCH --tasks-per-node=20                  # Número de cores que será utilizado
#SBATCH --nodes 1                          # Número de nós (computadores) que serão utilizados (1 para códigos openMP)
#SBATCH --time=30:00:00                    # Tempo máximo de simulação (D-HH:MM). 
#SBATCH -o slurm.%N.%j.out                 # Nome do arquivo onde a saída (stdout) será gravada %N = Máquina , %j = Número do trabalho. 
#SBATCH -e slurm.%N.%j.err                 # Nome do arquivo para qual a saída de erros  (stderr) será redirecionada.
#SBATCH --mail-user=widmark.cardoso@teg.ufsc.br            # Email para enviar notificações sobre alteração no estados do trabalho
#SBATCH --mail-type=BEGIN                  # Envia email quando o trabalho for iniciado
#SBATCH --mail-type=END                    # Envia email quando o trabalho finalizar
#SBATCH --mail-type=FAIL                   # Envia email caso o trabalho apresentar uma mensagem de erro.

module load openfoam.com/2112

source $WM_PROJECT_DIR/bin/tools/RunFunctions

#cp -ar 0.org 0

# --- Gera malha
#runApplication gmshToFoam circMesh.msh
runApplication gmshToFoam Mesh1_10Hz_8ppw.msh
runApplication changeDictionary 
#runApplication blockMesh

#--- Paralelização
runApplication decomposePar
#runParallel renumberMesh -overwrite

#--- Rodar simulação
runParallel $(getApplication)

#--- Pós-processamento
runApplication reconstructPar -latestTime
postProcess -latestTime -func probesSpacial > log.postProcessSpacial
# postProcess -func probesTime > log.postProcessTime

