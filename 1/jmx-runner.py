# -*- coding: utf-8 -*-
# author: zhangll

import os
import sys
import commands

if 'posix' in os.name:
    JMETER_BIN = '/usr/local/jmeter/bin/jmeter.sh -n -t '
else:
    JMETER_BIN = 'D:/opts/apache-jmeter-3.0/apache-jmeter-3.0/bin/jmeter-n.cmd'

ASSERT_FAIL_LISTENER_NAME = 'BeanShellListenerExitOnAssertFail'
ASSERT_FAIL_LISTENER_CONTENT = '''
<BeanShellListener guiclass="TestBeanGUI" testclass="BeanShellListener" testname="BeanShellListenerExitOnAssertFail" enabled="true">
<boolProp name="resetInterpreter">false</boolProp>
<stringProp name="parameters"></stringProp>
<stringProp name="filename"></stringProp>
<stringProp name="script">import org.apache.jmeter.assertions.AssertionResult;
AssertionResult[] results = sampleResult.getAssertionResults();
for(int i =0; i&lt;results.length; i++) { 
 AssertionResult result = results[i];
 boolean resultHasFailed = result.isFailure() || result.isError();
  if(resultHasFailed) {
  	String loginfo = &quot;###### &quot; + result.getName() + &quot; ######: &quot; + result.getFailureMessage();
  	System.out.println(loginfo);
        System.out.println(&quot;###simple###: &quot; + sampleResult.toString());
        System.out.println(&quot;###simple label###: &quot; + sampleResult.getSampleLabel());
        System.out.println(&quot;###response code###: &quot; + sampleResult.getResponseCode());
        System.out.println(&quot;###request headers###: &quot; + sampleResult.getRequestHeaders());
        System.out.println(&quot;###response headers###: &quot; + sampleResult.getResponseHeaders());
        System.out.println(&quot;###body size###: &quot; + sampleResult.getBodySize());
        System.out.println(&quot;###response end time###: &quot; + new java.util.Date(sampleResult.getEndTime()));
        System.out.println(&quot;###content###: &quot; + sampleResult.getResponseDataAsString());
  	System.exit(1);
  }
}
</stringProp>
</BeanShellListener>
<hashTree/>
'''
ASSERT_FAIL_LISTENER_CONTENT_AFTER_KEYWORD='<ThreadGroup'

def has_assertfail_exit_listener(jmx_path):
    with open(jmx_path, 'r') as fr:
        return ASSERT_FAIL_LISTENER_NAME in fr.read()

def append_assertfail_exit_listener(jmx_path):
    jmx_content = None
    with open(jmx_path, 'r') as fr:
        jmx_content = fr.read()

    jmx_content = jmx_content.replace(ASSERT_FAIL_LISTENER_CONTENT_AFTER_KEYWORD, ASSERT_FAIL_LISTENER_CONTENT + ASSERT_FAIL_LISTENER_CONTENT_AFTER_KEYWORD)

    with open(jmx_path, 'w') as fw:
        fw.write(jmx_content)

def execute_jmx(jmx_path):
    command = '%s %s' %(JMETER_BIN, jmx_path)
    print command
    status = os.system(command)
    if status !=0:
        sys.exit(1)

def main(jmx_path):
    if not has_assertfail_exit_listener(jmx_path):
        append_assertfail_exit_listener(jmx_path)

    execute_jmx(jmx_path)

if __name__ == "__main__":
    jmx_path = sys.argv[1]
    main(jmx_path)
