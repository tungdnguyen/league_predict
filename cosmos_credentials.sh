RES_GROUP=league
ACCT_NAME=lolpredict
export ACCOUNT_URI=$(az cosmosdb show --resource-group $RES_GROUP --name $ACCT_NAME --query documentEndpoint --output tsv)
export ACCOUNT_KEY=$(az cosmosdb keys list --resource-group $RES_GROUP --name $ACCT_NAME --query primaryMasterKey --output tsv)
