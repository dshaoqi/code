#include<stdio.h>
#include<stdlib.h>
#include<libssh/libssh.h>
#include<string.h>
int verify_host(ssh_session ss);
int verify_user(ssh_session ss,char *password);
int carryout_command(ssh_session ss,char *command);

char hostfile[]="/root/C/ssh/host.txt";

ssh_session get_session(char *ip,int port,char *user);

int simplessh(char *ip,char *user,char *password,char *command);


int main(){
    simplessh("localhost","root","dsq","ps -ef");
	return 1;
}


int verify_host(ssh_session ss){
    unsigned char *hash = NULL;
    ssh_key srv_pubkey = NULL;
    char buff[10];
    size_t hlen;
    char *hexa;
    int rc;
    
    if(ssh_get_server_publickey(ss,&srv_pubkey)<0){
        return -1;
    }
    if(ssh_get_publickey_hash(srv_pubkey,SSH_PUBLICKEY_HASH_SHA1,&hash,&hlen)<0){
        return -1;
    }
    hexa = ssh_get_hexa(hash,hlen);
    switch(ssh_session_is_known_server(ss)){
        case SSH_KNOWN_HOSTS_OK:
            //printf("known hosts\n");
            return 1;
        case SSH_KNOWN_HOSTS_CHANGED:
            printf("host key chaged\n");
            printf("the new key hash is:%s\n",hexa);
            return -1;
        case SSH_KNOWN_HOSTS_UNKNOWN:
            printf("the server is unknown, Do you trust\n");
            printf("the key hash is:%s\n",hexa);
            if(ssh_session_update_known_hosts(ss)<0){
                printf("update known_hosts file failed\n");
                return -1;
            }
            return 1;
        case SSH_KNOWN_HOSTS_NOT_FOUND:
            printf("could not find host file\n");
            return -1;
        default:
            printf("enter case default\n");
            return -1;
    }
    ssh_clean_pubkey_hash(&hash);
    return -1;
}

int verify_user(ssh_session ss,char *password){
    //char *password = getpass("Password: ");
    if(ssh_userauth_password(ss,NULL,password)!=SSH_AUTH_SUCCESS){
        printf("auth user failed\n");
        return -1;
    }
    return 1;
}


int carryout_command(ssh_session ss,char *command){
    ssh_channel ch;
    int rc;
    char buffer[1024];
    int nbytes;
    ch = ssh_channel_new(ss);
    if(ch == NULL){
        printf("ssh_channel_new wrong\n");
        return -1;
    }

    if(ssh_channel_open_session(ch)!=SSH_OK){
        printf("ssh_channel_open_session wrong\n");
        return -1;
    }

    if(ssh_channel_request_exec(ch,command)!=SSH_OK){
        printf("ssh_channel_request_exec wrong\n");
        return -1;
    }
    
    while(1){
        nbytes=ssh_channel_read(ch,buffer,sizeof(buffer),0);
        if(nbytes!=0&&nbytes!=SSH_ERROR){
            write(1,buffer,nbytes);
        }
        else break;
    }
    return 1;
}




ssh_session get_session(char *ip,int port,char *user){
    ssh_session ss=ssh_new();
    if(ss==NULL){
        printf("ssh_new error\n");
        exit(-1);
    }
    ssh_options_set(ss,SSH_OPTIONS_HOST,"localhost");
    ssh_options_set(ss,SSH_OPTIONS_USER,user);
    ssh_options_set(ss,SSH_OPTIONS_LOG_VERBOSITY,SSH_LOG_NOLOG);
    ssh_options_set(ss,SSH_OPTIONS_PORT,&port);
    if(ssh_connect(ss)!=SSH_OK){
        printf("ssh_connect error\n");
        exit(-1);
    }
    else{
        return ss;
    }
}


int simplessh(char *ip,char *user,char *password,char *command){
    ssh_session ss = get_session(ip,22,user);
    if(verify_host(ss)==-1){
        printf("verify host not pass\n");
    }
    verify_user(ss,password);
    carryout_command(ss,command);
    ssh_disconnect(ss);
    ssh_free(ss);

}
